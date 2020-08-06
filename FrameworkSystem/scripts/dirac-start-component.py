#!/usr/bin/env python
"""
Start DIRAC component using runsvctrl utility
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

__RCSID__ = "$Id$"

from DIRAC.Core.Base import Script
Script.disableCS()
Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                  'Usage:',
                                  '  %s [option|cfgfile] ... [system [service|agent]]' % Script.scriptName,
                                  'Arguments:',
                                  '  system:        Name of the system for the component (default *: all)',
                                  '  service|agent: Name of the particular component (default *: all)']))
Script.parseCommandLine()
args = Script.getPositionalArgs()
if len(args) > 2:
  Script.showHelp(1)

system = '*'
component = '*'
if len(args) > 0:
  system = args[0]
if system != '*':
  if len(args) > 1:
    component = args[1]
#
from DIRAC.FrameworkSystem.Client.ComponentInstaller import gComponentInstaller
#
gComponentInstaller.exitOnError = True
#
result = gComponentInstaller.runsvctrlComponent(system, component, 'u')
if not result['OK']:
  print('ERROR:', result['Message'])
  exit(-1)

gComponentInstaller.printStartupStatus(result['Value'])
