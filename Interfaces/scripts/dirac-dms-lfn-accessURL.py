#!/usr/bin/env python
########################################################################
# $HeadURL$
# File :    dirac-dms-lfn-accessURL
# Author :  Stuart Paterson
########################################################################
"""
  Retrieve an access URL for an LFN replica given a valid DIRAC SE.
"""
from __future__ import print_function
__RCSID__ = "$Id$"
import DIRAC
from DIRAC.Core.Base import Script

Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                  'Usage:',
                                  '  %s [option|cfgfile] ... LFN SE [PROTO]' % Script.scriptName,
                                  'Arguments:',
                                  '  LFN:      Logical File Name or file containing LFNs',
                                  '  SE:       Valid DIRAC SE',
                                  '  PROTO:    Optional protocol for accessURL']))
Script.parseCommandLine(ignoreErrors=True)
args = Script.getPositionalArgs()

# pylint: disable=wrong-import-position
from DIRAC.Interfaces.API.Dirac import Dirac

if len(args) < 2:
  Script.showHelp()

if len(args) > 3:
  print('Only one LFN SE pair will be considered')

dirac = Dirac()
exitCode = 0

lfn = args[0]
seName = args[1]
proto = False
if len(args) > 2:
  proto = args[2]

try:
  f = open(lfn, 'r')
  lfns = f.read().splitlines()
  f.close()
except IOError:
  lfns = [lfn]

for lfn in lfns:
  result = dirac.getAccessURL(lfn, seName, protocol=proto, printOutput=True)
  if not result['OK']:
    print('ERROR: ', result['Message'])
    exitCode = 2

DIRAC.exit(exitCode)
