""" DIRAC Multi VO FileCatalog plugin class to manage file metadata for multiple VO.
"""

__RCSID__ = "$Id$"

from DIRAC.DataManagementSystem.DB.FileCatalogComponents.FileMetadata import FileMetadata
from DIRAC.DataManagementSystem.DB.FileCatalogComponents.MultiVOMetaNameMixIn import MultiVOMetaNameMixIn

class MultiVOFileMetadata(MultiVOMetaNameMixIn, FileMetadata):
  """
  MULti-VO FileCatalog plugin implementation.
  """

  def __init__(self, database=None):
    FileMetadata.__init__(self, database=database)
    MultiVOMetaNameMixIn.__init__(self)

