""" DIRAC Multi VO FileCatalog plugin class to manage file metadata for multiple VO.
"""

__RCSID__ = "$Id$"

from FileMetadata import FileMetadata


class MultiVOFileMetadata(FileMetadata):
  """
  MULti-VO FileCatalog plugin implementation.
  """

  def __init__(self, database=None):
    FileMetadata.__init__(self, database=database)

  def getMetaName(self, meta, credDict):
    """
    Return a fully-qualified metadata name based on client-suplied metadata name and
    client credentials. User group is added to the metadata passed in.
    :param meta: metadata name
    :param credDict: client credentials
    :return: fully-qualified metadata name
    """

    return meta + self.getMetaNameSuffix(credDict)

  def getMetaNameSuffix(self, credDict):
    """
    Get a VO specific suffix from user credentials.
    :param credDict: user credentials
    :return: VO specific suffix
    """
    return '_' + credDict['group']
