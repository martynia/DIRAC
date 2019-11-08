# $HeadURL: $
""" PilotEfficiencyPolicy

  Policy that calculates the efficiency following the formula::

    done / ( failed + aborted + done )

  if the denominator is smaller than 10, it does not take any decision.
"""

from __future__ import division
from DIRAC                                              import S_OK
from DIRAC.ResourceStatusSystem.PolicySystem.PolicyBase import PolicyBase

__RCSID__ = '$Id: $'

class PilotEfficiencyPolicy( PolicyBase ):
  """ PilotEfficiencyPolicy class, extends PolicyBase
  """

  @staticmethod
  def _evaluate( commandResult ):
    """ _evaluate

    efficiency < 0.5 :: Banned
    efficiency < 0.9 :: Degraded

    """

    minTotal = 10
    result = {
               'Status' : None,
               'Reason' : None
              }

    if not commandResult[ 'OK' ]:
      result[ 'Status' ] = 'Error'
      result[ 'Reason' ] = commandResult[ 'Message' ]
      return S_OK( result )

    commandResult = commandResult[ 'Value' ]

    if not commandResult:
      result[ 'Status' ] = 'Unknown'
      result[ 'Reason' ] = 'No values to take a decision'
      return S_OK( result )

    commandResult = commandResult[ 0 ]

    if not commandResult:
      result[ 'Status' ] = 'Unknown'
      result[ 'Reason' ] = 'No values to take a decision'
      return S_OK( result )

    # Pilot efficiency is now available directly from the command result, in percent:
    efficiency = commandResult.get('PilotJobEff', None)

    if efficiency is None:
      result[ 'Status' ] = 'Unknown'
      result[ 'Reason' ] = 'Pilot efficiency value is not present in the result obtained'
      return S_OK(result)

    """
    aborted = commandResult.get('Aborted', 0)
    #deleted = float( commandResult[ 'Deleted' ] )
    done    = commandResult.get('Done', 0)
    failed  = commandResult.get('Failed', 0)

    #total     = aborted + deleted + done + failed
    total     = aborted + done + failed

    #we want a minimum amount of pilots to take a decision ( at least 10 pilots )
    if total < minTotal:
      result[ 'Status' ] = 'Unknown'
      result[ 'Reason' ] = 'Not enough pilots (%d) to take a decision (<%d)' % (total, minTotal)
      return S_OK( result )

    efficiency = done / total
    """
    if efficiency <= 50.0:
      result[ 'Status' ] = 'Banned'
    elif efficiency <= 90.0:
      result[ 'Status' ] = 'Degraded'
    else:
      result[ 'Status' ] = 'Active'

    result[ 'Reason' ] = 'Pilots Efficiency of %.2f' % efficiency
    return S_OK( result )

#...............................................................................
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF
