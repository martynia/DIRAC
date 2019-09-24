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


class RucioFileCatalogClient(FileCatalogClientBase):
  """

  """

  READ_METHODS = FileCatalogClientBase.READ_METHODS + ['listDirectory', 'getUserDirectory']


  WRITE_METHODS = FileCatalogClientBase.WRITE_METHODS + ['addFile']

  NO_LFN_METHODS = FileCatalogClientBase.NO_LFN_METHODS + ['getUserDirectory', 'createUserDirectory',
                                                         'createUserMapping', 'removeUserDirectory']

  ADMIN_METHODS = FileCatalogClientBase.ADMIN_METHODS + ['getUserDirectory']

  def __init__( self, url=None,  **options ):
    self.serverURL = 'DataManagement/RucioFileCatalog' if not url else url
    super(RucioFileCatalogClient, self).__init__(self.serverURL, **options)
    gLogger.debug("Rucio File Catalog client created with options: ", options)

  @checkCatalogArguments
  def listDirectory( self, lfns, verbose = False ):
    gLogger.debug("Rucio list directory for lfns: ", lfns)
    if verbose:
      pass

  @checkCatalogArguments
  def isFile(self, lfns, timeout=120):
    """ Check whether the supplied lfns are files """
    gLogger.debug("Rucio is file (lfns): ", lfns)
    return self._getRPC(timeout=timeout).isFile(lfns)