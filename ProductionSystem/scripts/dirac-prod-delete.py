#!/usr/bin/env python

"""
  Delete a given production
"""

__RCSID__ = "$Id$"

import DIRAC
from DIRAC.Core.Base import Script

Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                  'Usage:',
                                  '  %s prodID' % Script.scriptName,
                                  'Arguments:',
                                  '  prodID: Production ID'
                                  ]))


Script.parseCommandLine()

from DIRAC.ProductionSystem.Client.ProductionClient import ProductionClient

args = Script.getPositionalArgs()
if (len(args) != 1):
  Script.showHelp()

# get arguments
prodID = args[0]

prodClient = ProductionClient()

res = prodClient.deleteProduction(prodID)
if res['OK']:
  DIRAC.gLogger.notice('Production %s successully deleted' % prodID)
else:
  DIRAC.gLogger.error(res['Message'])
  DIRAC.exit(-1)

DIRAC.exit(0)
