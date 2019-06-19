""" DIRAC Multi VO MixIn class to manage file metadata and directory for multiple VO.
"""

__RCSID__ = "$Id$"

from DIRAC.DataManagementSystem.DB.FileCatalogComponents.MetaNameMixIn import MetaNameMixIn
from DIRAC.ConfigurationSystem.Client.Helpers import Registry


class MultiVOMetaNameMixIn(MetaNameMixIn):
  """
  MULti-VO MetaName MixIn implementation.
  """

  def __init__(self):
    MetaNameMixIn.__init__(self)

  def getMetaName(self, meta, credDict):
    """
    Return a fully-qualified metadata name based on client-suplied metadata name and
    client credentials. User group is added to the metadata passed in.

    :param meta: metadata name
    :param credDict: client credentials
    :return: fully-qualified metadata name
    """

    return meta + self._getMetaNameSuffix(credDict)

  def getMetaNameSuffix(self, credDict):
    """
    Get a VO specific suffix from user credentials.

    :param credDict: user credentials
    :return: VO specific suffix
    """
    vo = Registry.getGroupOption(credDict['group'], 'VO')
    return '_' + vo.replace('-','_')

