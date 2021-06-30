""" :mod: RucioRSSAgent

    Agent that synchronizes Rucio and Dirac
"""

# # imports
from traceback import format_exc

from DIRAC import S_OK, S_ERROR
from DIRAC import gLogger
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.Core.Security import Locations
from DIRAC.ConfigurationSystem.Client.Helpers.Registry import getVOs
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.ResourceStatusSystem.Client.ResourceStatus import ResourceStatus

from rucio.client import Client

__RCSID__ = "Id$"

class RucioRSSAgent(AgentModule):
  """
  .. class:: RucioRSSAgent

  Agent that synchronizes Rucio and Dirac
  """

  def initialize(self):
    """ agent's initalisation

    :param self: self reference
    """
    self.log =  gLogger.getSubLogger('RucioRSS')
    self.log.info("Starting RucioRSSAgent")
    # CA location
    self.caCertPath = Locations.getCAsLocation()
    # configured VOs
    res = getVOs()
    if res['OK']:
      voList = getVOs().get('Value', [])
    else:
      return S_ERROR(res['Message'])

    if isinstance(voList, str):
      voList = [voList]
    self.clientConfig = {}
    self.log.debug("VO list to consider for RSS->RSE synchronization: ", voList)
    # get VO-specific Rucio parameters for the Operations section:
    for vo in voList:
      opHelper = Operations(vo=vo)
      # TODO determine 'RucioFileCatalog' type from resources
      fileCatalogs = opHelper.getValue('/Services/Catalogs/CatalogList', [])
      # if the list is not empty it has to contain RucioFileCatalog
      if fileCatalogs and 'RucioFileCatalog' not in fileCatalogs:
        self.log.warn("%s VO is not using RucioFileCatalog - it is not in the catalog list" % vo)
        continue
      params = {}
      result = opHelper.getOptionsDict('/Services/Catalogs/RucioFileCatalog')
      if result['OK']:
        optDict = result['Value']
        params['rucioHost'] = optDict.get('RucioHost', None)
        params['authHost'] = optDict.get('AuthHost', None)
        params['privilegedAccount'] = optDict.get('PrivilegedAccount', 'root')
        self.clientConfig[vo] = params
        self.log.info('RSEs status will be set/updated in Rucio for the %s VO ' % vo)
      else:
        self.log.warn("No Services/Catalogs/RucioFileCatalog for VO %s (VO skipped)" % vo)
    self.log.debug(" VO-specific Rucio Client config parameters: ", self.clientConfig)
    return S_OK()

  def execute(self):
    """
    Perform RSS->RSE synchronisation for all eligible VOs.

    :return: S_OK or S_ERROR
    """
    voRes = {}
    for key in self.clientConfig:
      result = self.executeForVO(key)
      voRes[key] = result['OK']

    product = all(list(voRes.values()))
    if product:
      return S_OK()
    else:
      message = "RSS -> RSE synchronisation for at least one VO among eligible VOs was NOT successful."
      self.log.info(message)
      self.log.debug(voRes)
      return S_ERROR(message)

  def executeForVO(self, vo):
    """ execution in one agent's cycle

    :param self: self reference
    """
    rSS = ResourceStatus()

    try:
      try:
        self.log.info('Login to Rucio as privileged user with host cert/key')
        certKeyTuple = Locations.getHostCertificateAndKeyLocation()
        if not certKeyTuple:
          self.log.error("Hostcert/key location not set")
          return S_ERROR("Hostcert/key location not set")
        hostcert, hostkey = certKeyTuple

        self.log.info("Logging in with a host cert/key pair:")
        self.log.debug('account: ', self.clientConfig[vo]['privilegedAccount'])
        self.log.debug('rucio host: ', self.clientConfig[vo]['rucioHost'])
        self.log.debug('auth  host: ', self.clientConfig[vo]['authHost'])
        self.log.debug('CA cert path: ', self.caCertPath)
        self.log.debug('Cert location: ', hostcert)
        self.log.debug('Key location: ', hostkey)
        self.log.debug('VO: ', vo)

        client = Client(account=self.clientConfig[vo]['privilegedAccount'],
                        rucio_host=self.clientConfig[vo]['rucioHost'],
                        auth_host=self.clientConfig[vo]['authHost'],
                        ca_cert=self.caCertPath,
                        auth_type='x509',
                        creds={'client_cert': hostcert, 'client_key': hostkey},
                        timeout=600,
                        user_agent='rucio-clients', vo=vo)
      except Exception as err:
        self.log.info('Login to Rucio as privileged user with host cert/key failed. Try username/password')
        client = Client(account='root', auth_type='userpass')
    except Exception:
    # login exception, skip this VO
      self.log.error(" Login for %s VO failed. VO skipped " % vo)
      self.log.error(str(format_exc()))
      return S_ERROR(str(format_exc()))

    self.log.info(" Rucio login successful - continue with synchronisation")
    return S_OK()
    try:
      for rse in client.list_rses():
        thisSe = rse['rse']
        self.log.info("Running on %s", thisSe)
        resStatus = rSS.getElementStatus(thisSe, "StorageElement")
        dictSe = client.get_rse(thisSe)
        if resStatus['OK']:
          seAccessValue = resStatus['Value'][thisSe]
          availabilityRead = True if seAccessValue['ReadAccess'] in ['Active', 'Degraded'] else False
          availabilityWrite = True if seAccessValue['WriteAccess'] in ['Active', 'Degraded'] else False
          availabilityDelete = True if seAccessValue['RemoveAccess'] in ['Active', 'Degraded'] else False
          isUpdated = False
          if dictSe['availability_read'] != availabilityRead:
            self.log.info('Set availability_read for %s to %s', thisSe, availabilityRead)
            client.update_rse(thisSe, {'availability_read': availabilityRead})
            isUpdated = True
          if dictSe['availability_write'] != availabilityWrite:
            self.log.info('Set availability_write for %s to %s', thisSe, availabilityWrite)
            client.update_rse(thisSe, {'availability_write': availabilityWrite})
            isUpdated = True
          if dictSe['availability_delete'] != availabilityDelete:
            self.log.info('Set availability_delete for %s to %s', thisSe, availabilityDelete)
            client.update_rse(thisSe, {'availability_delete': availabilityDelete})
            isUpdated = True
    except Exception as err:
      return S_ERROR(str(err))
    return S_OK()
