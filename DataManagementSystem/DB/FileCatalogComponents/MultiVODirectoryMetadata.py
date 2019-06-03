""" DIRAC Multi VO FileCatalog plugin class to manage file metadata for multiple VO.
"""

__RCSID__ = "$Id$"

from DirectoryMetadata import DirectoryMetadata
from DIRAC.ConfigurationSystem.Client.Helpers import Registry


class MultiVODirectoryMetadata(DirectoryMetadata):
  """
  MULti-VO FileCatalog plugin implementation.
  """

  def __init__(self, database=None):
    DirectoryMetadata.__init__(self, database=database)

  def getMetaName(self, meta, credDict):
    """
    Return a fully-qualified metadata name based on client-suplied metadata name and
    client credentials. User VO is added to the metadata passed in.

    :param meta: metadata name
    :param credDict: client credentials
    :return: fully-qualified metadata name
    """

    return meta + self.getMetaNameSuffix(credDict)

  def getMetaNameSuffix(self, credDict):
    """
    Get a VO specific suffix from user credentials and the CS.

    :param credDict: user credentials
    :return: VO specific suffix
    """

    vo = Registry.getGroupOption(credDict['group'], 'VO')
    return '_' + vo
