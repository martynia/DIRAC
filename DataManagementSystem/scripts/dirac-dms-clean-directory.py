#! /usr/bin/env python

__RCSID__ = "$Id$"

import os
import sys

from DIRAC import exit as DIRACExit, gLogger
from DIRAC.Core.Base import Script

Script.setUsageMessage("""
Clean the given directory or a list of directories by removing it and all the
contained files and subdirectories from the physical storage and from the
file catalogs.

Usage:
   %s <LFN_Directory | fileContainingLFN_Directories>
""" % Script.scriptName)

Script.parseCommandLine()

args = Script.getPositionalArgs()
if len(args) != 1:
  Script.showHelp()
  DIRACExit(-1)

inputFileName = args[0]

if os.path.exists(inputFileName):
  lfns = [lfn.strip().split()[0] for lfn in sorted(open(inputFileName, 'r').read().splitlines())]
else:
  lfns = [inputFileName]

from DIRAC.DataManagementSystem.Client.DataManager import DataManager
dm = DataManager()
retVal = 0
for lfn in [lfn for lfn in lfns if lfn]:
  gLogger.notice("Cleaning directory %r ... " % lfn)
  result = dm.cleanLogicalDirectory(lfn)
  if not result['OK']:
    gLogger.error('Failed to clean directory', result['Message'])
    retVal = -1
  else:
    if not result['Value']['Failed']:
      gLogger.notice('OK')
    else:
      for folder, message in result['Value']['Failed'].items():
        gLogger.error('Failed to clean folder', "%r: %s" % (folder, message))
        retVal = -1

  DIRACExit(retVal)
