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

  READ_METHODS = ['listDirectory', 'getUserDirectory']


  WRITE_METHODS = ['addFile']

  NO_LFN_METHODS =  ['getUserDirectory', 'createUserDirectory',
                                                         'createUserMapping', 'removeUserDirectory']

  ADMIN_METHODS =  ['getUserDirectory']

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