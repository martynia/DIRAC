""" DIRAC Multi VO FileCatalog plugin class to manage file metadata for multiple VO.
"""

__RCSID__ = "$Id$"

from DIRAC.DataManagementSystem.DB.FileCatalogComponents.FileMetadata import FileMetadata
from DIRAC.ConfigurationSystem.Client.Helpers import Registry


class MultiVOFileMetadata(FileMetadata):
  """
  MULti-VO FileCatalog plugin implementation.
  """

  def __init__(self, database=None):
    FileMetadata.__init__(self, database=database)

  def _getMetaName(self, meta, credDict):
    """
    Return a fully-qualified metadata name based on client-suplied metadata name and
    client credentials. User group is added to the metadata passed in.

    :param meta: metadata name
    :param credDict: client credentials
    :return: fully-qualified metadata name
    """

    return meta + self._getMetaNameSuffix(credDict)

  def _getMetaNameSuffix(self, credDict):
    """
    Get a VO specific suffix from user credentials.

    :param credDict: user credentials
    :return: VO specific suffix
    """
    vo = Registry.getGroupOption(credDict['group'], 'VO')
    return '_' + vo
