"""
Rucio File Catalog Client.
"""

from __future__ import division

import os

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Resources.Catalog.Utilities import checkCatalogArguments
from DIRAC.ConfigurationSystem.Client.Helpers.Registry import getDNForUsername, getVOMSAttributeForGroup, \
  getVOForGroup, getVOOption
from DIRAC.Resources.Catalog.FileCatalogClientBase import FileCatalogClientBase
from DIRAC.Core.Base.Client import Client

class RucioFileCatalogClient(FileCatalogClientBase):
  """

  """

  READ_METHODS = FileCatalogClientBase.READ_METHODS + ['listDirectory', 'getUserDirectory']


  WRITE_METHODS = FileCatalogClientBase.WRITE_METHODS + ['addFile']

  NO_LFN_METHODS =  FileCatalogClientBase.NO_LFN_METHODS + ['getUserDirectory', 'createUserDirectory',
                                                         'createUserMapping', 'removeUserDirectory']

  ADMIN_METHODS =  FileCatalogClientBase.ADMIN_METHODS + ['getUserDirectory']

  def __init__( self, url=None,  **options ):
    #self.serverURL = 'DataManagement/RucioFileCatalog' if not url else url
    super(RucioFileCatalogClient, self).__init__(self.serverURL, **options)
    gLogger.debug("Rucio File Catalog client created with options: ", options)

  @checkCatalogArguments
  def listDirectory( self, lfns, verbose = False ):
    gLogger.debug("Rucio list directory for lfns: ", lfns)
    if verbose:
      pass
    return S_OK({'Failed':[], 'Successful':[]})

  @checkCatalogArguments
  def isFile(self, lfns, verbose=False):
    """ Check whether the supplied lfns are files """
    gLogger.debug("Rucio is file (lfns): ", lfns)
    if verbose:
       pass
    return S_OK({'Failed':[], 'Successful':[]})

  @checkCatalogArguments
  def addFile( self, lfns ):
    """
    Upload and register a local file with Rucio file catalog.

    :param lfns:
    :return:
    """
    successful = {}
    gLogger.debug("Rucio addFile (lfns): ", lfns)
    for lfn  in lfns:
      lfnInfo = lfns[lfn]
      pfn = lfnInfo['PFN']
      size = lfnInfo['Size']
      se = lfnInfo['SE']
      guid = lfnInfo['GUID']
      checksum = lfnInfo['Checksum']
      scope = lfnInfo.split('/')[2]

    return S_OK({'Failed':{}, 'Successful':{}})

  @checkCatalogArguments
  def hasAccess(self, lfns, opType ):

    if opType in RucioFileCatalogClient.READ_METHODS:
      opType = 'Read'
    elif opType in RucioFileCatalogClient.WRITE_METHODS:
      opType = 'Write'

    failed = {}
    successful = dict( ( path, True ) for path in lfns )

    return S_OK( {'Successful': successful, 'Failed' : failed} )
  