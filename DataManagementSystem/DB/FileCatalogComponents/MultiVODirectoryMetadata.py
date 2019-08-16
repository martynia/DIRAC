""" DIRAC Multi VO FileCatalog plugin class to manage directory metadata for multiple VO.
"""

__RCSID__ = "$Id$"

from DIRAC.DataManagementSystem.DB.FileCatalogComponents.DirectoryMetadata import DirectoryMetadata
from DIRAC.DataManagementSystem.DB.FileCatalogComponents.MultiVOMetaNameMixIn import MultiVOMetaNameMixIn


class MultiVODirectoryMetadata(MultiVOMetaNameMixIn, DirectoryMetadata):
  """
  MULti-VO FileCatalog plugin implementation.
  """

  def __init__(self, database=None):
    super(MultiVODirectoryMetadata, self).__init__(database=database)

