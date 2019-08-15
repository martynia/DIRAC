########################################################################
# $HeadURL $
# File: PhysicalRemoval.py
# Author: Krzysztof.Ciba@NOSPAMgmail.com
# Date: 2013/04/02 11:56:10
########################################################################
""" :mod: PhysicalRemoval

    =====================

    .. module: PhysicalRemoval

    :synopsis: PhysicalRemoval operation handler

    .. moduleauthor:: Krzysztof.Ciba@NOSPAMgmail.com

    PhysicalRemoval operation handler
"""

__RCSID__ = "$Id $"

# #
# @file PhysicalRemoval.py
# @author Krzysztof.Ciba@NOSPAMgmail.com
# @date 2013/04/02 11:56:22
# @brief Definition of PhysicalRemoval class.

# # imports
import os
import time
import datetime
import socket
# # from DIRAC
from DIRAC import S_OK
from DIRAC.FrameworkSystem.Client.MonitoringClient import gMonitor
from DIRAC.DataManagementSystem.Agent.RequestOperations.DMSRequestOperationsBase import DMSRequestOperationsBase
from DIRAC.Resources.Storage.StorageElement import StorageElement

from DIRAC.MonitoringSystem.Client.MonitoringReporter import MonitoringReporter
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations

########################################################################


class PhysicalRemoval(DMSRequestOperationsBase):
  """
  .. class:: PhysicalRemoval

  """

  def __init__(self, operation=None, csPath=None):
    """c'tor

    :param self: self reference
    :param ~DIRAC.RequestManagementSystem.Client.Operation.Operation operation: Operation instance
    :param str csPath: cs config path
    """
    DMSRequestOperationsBase.__init__(self, operation, csPath)
<<<<<<< HEAD
    # # gMonitor stuff
    gMonitor.registerActivity("PhysicalRemovalAtt", "Physical file removals attempted",
                              "RequestExecutingAgent", "Files/min", gMonitor.OP_SUM)
    gMonitor.registerActivity("PhysicalRemovalOK", "Successful file physical removals",
                              "RequestExecutingAgent", "Files/min", gMonitor.OP_SUM)
    gMonitor.registerActivity("PhysicalRemovalFail", "Failed file physical removals",
                              "RequestExecutingAgent", "Files/min", gMonitor.OP_SUM)
    gMonitor.registerActivity("PhysicalRemovalSize", "Physically removed size",
                              "RequestExecutingAgent", "Bytes", gMonitor.OP_ACUM)
=======

    # Check whether the ES flag is enabled so we can send the data accordingly.
    self.rmsMonitoring = Operations().getValue("EnableActivityMonitoring", False)

    if self.rmsMonitoring:
      self.rmsMonitoringReporter = MonitoringReporter(monitoringType="RMSMonitoring")
    else:
      # # gMonitor stuff
      gMonitor.registerActivity("PhysicalRemovalAtt", "Physical file removals attempted",
                                "RequestExecutingAgent", "Files/min", gMonitor.OP_SUM)
      gMonitor.registerActivity("PhysicalRemovalOK", "Successful file physical removals",
                                "RequestExecutingAgent", "Files/min", gMonitor.OP_SUM)
      gMonitor.registerActivity("PhysicalRemovalFail", "Failed file physical removals",
                                "RequestExecutingAgent", "Files/min", gMonitor.OP_SUM)
      gMonitor.registerActivity("PhysicalRemovalSize", "Physically removed size",
                                "RequestExecutingAgent", "Bytes", gMonitor.OP_ACUM)
>>>>>>> Migrate DMS/Agent/RequestOperations to ES.

  def __call__(self):
    """ perform physical removal operation """
    bannedTargets = self.checkSEsRSS(access='RemoveAccess')
    if not bannedTargets['OK']:
<<<<<<< HEAD
      gMonitor.addMark("PhysicalRemovalAtt")
      gMonitor.addMark("PhysicalRemovalFail")
=======
      if self.rmsMonitoring:
        for opFile in self.operation:
          for status in ["FileAttempted", "FileFailed"]:
            self.rmsMonitoringReporter.addRecord({
                "timestamp": time.mktime(datetime.datetime.utcnow().timetuple()),
                "host": socket.getfqdn(),
                "objectType": "File",
                "operationType": self.operation.Type,
                "objectID": opFile.FileID,
                "parentID": self.operation.OperationID,
                "status": status,
                "nbObject": 1
            })
        self.rmsMonitoringReporter.commit()
      else:
        gMonitor.addMark("PhysicalRemovalAtt")
        gMonitor.addMark("PhysicalRemovalFail")
>>>>>>> Migrate DMS/Agent/RequestOperations to ES.
      return bannedTargets

    if bannedTargets['Value']:
      return S_OK("%s targets are banned for removal" % ",".join(bannedTargets['Value']))

    # # get waiting files
    waitingFiles = self.getWaitingFilesList()
    # # prepare lfn dict
    toRemoveDict = dict((opFile.LFN, opFile) for opFile in waitingFiles)

    targetSEs = self.operation.targetSEList
<<<<<<< HEAD
    gMonitor.addMark("PhysicalRemovalAtt", len(toRemoveDict) * len(targetSEs))
=======

    if self.rmsMonitoring:
      for opFile in toRemoveDict.values():
        self.rmsMonitoringReporter.addRecord({
            "timestamp": time.mktime(datetime.datetime.utcnow().timetuple()),
            "host": socket.getfqdn(),
            "objectType": "File",
            "operationType": self.operation.Type,
            "objectID": opFile.FileID,
            "parentID": self.operation.OperationID,
            "status": "FileAttempted",
            "nbObject": len(targetSEs)
        })
      self.rmsMonitoringReporter.commit()
    else:
      gMonitor.addMark("PhysicalRemovalAtt", len(toRemoveDict) * len(targetSEs))
>>>>>>> Migrate DMS/Agent/RequestOperations to ES.

    # # keep errors dict
    removalStatus = dict.fromkeys(toRemoveDict.keys(), None)
    for lfn in removalStatus:
      removalStatus[lfn] = dict.fromkeys(targetSEs, "")

    for targetSE in targetSEs:

      self.log.info("removing files from %s" % targetSE)

      # # 1st - bulk removal
      bulkRemoval = self.bulkRemoval(toRemoveDict, targetSE)
      if not bulkRemoval["OK"]:
        self.log.error('Failed bulk removal', bulkRemoval["Message"])
        self.operation.Error = bulkRemoval["Message"]
        return bulkRemoval

      bulkRemoval = bulkRemoval["Value"]

      for lfn, opFile in toRemoveDict.items():
        removalStatus[lfn][targetSE] = bulkRemoval["Failed"].get(lfn, "")
        opFile.Error = removalStatus[lfn][targetSE]

      # # 2nd - single file removal
      toRetry = dict((lfn, opFile) for lfn, opFile in toRemoveDict.items() if lfn in bulkRemoval["Failed"])
      for lfn, opFile in toRetry.items():
        self.singleRemoval(opFile, targetSE)
        if not opFile.Error:
          removalStatus[lfn][targetSE] = ""
        else:
<<<<<<< HEAD
          gMonitor.addMark("PhysicalRemovalFail", 1)
=======
          if self.rmsMonitoring:
            self.rmsMonitoringReporter.addRecord({
                "timestamp": time.mktime(datetime.datetime.utcnow().timetuple()),
                "host": socket.getfqdn(),
                "objectType": "File",
                "operationType": self.operation.Type,
                "objectID": opFile.FileID,
                "parentID": self.operation.OperationID,
                "status": "FileFailed",
                "nbObject": 1
            })
          else:
            gMonitor.addMark("PhysicalRemovalFail", 1)
>>>>>>> Migrate DMS/Agent/RequestOperations to ES.
          removalStatus[lfn][targetSE] = opFile.Error

    # # update file status for waiting files
    failed = 0
    for opFile in self.operation:
      if opFile.Status == "Waiting":
        errors = [error for error in removalStatus[opFile.LFN].values() if error.strip()]
        if errors:
          failed += 1
          opFile.Error = ",".join(errors)
          if "Write access not permitted for this credential" in opFile.Error:
            opFile.Status = "Failed"
<<<<<<< HEAD
            gMonitor.addMark("PhysicalRemovalFail", len(errors))
          continue
        gMonitor.addMark("PhysicalRemovalOK", len(targetSEs))
        gMonitor.addMark("PhysicalRemovalSize", opFile.Size * len(targetSEs))
=======

            if self.rmsMonitoring:
              self.rmsMonitoringReporter.addRecord({
                  "timestamp": time.mktime(datetime.datetime.utcnow().timetuple()),
                  "host": socket.getfqdn(),
                  "objectType": "File",
                  "operationType": self.operation.Type,
                  "objectID": opFile.FileID,
                  "parentID": self.operation.OperationID,
                  "status": "FileFailed",
                  "nbObject": len(errors)
              })
            else:
              gMonitor.addMark("PhysicalRemovalFail", len(errors))

          continue

        if self.rmsMonitoring:
          self.rmsMonitoringReporter.addRecord({
              "timestamp": time.mktime(datetime.datetime.utcnow().timetuple()),
              "host": socket.getfqdn(),
              "objectType": "File",
              "operationType": self.operation.Type,
              "objectID": opFile.FileID,
              "parentID": self.operation.OperationID,
              "status": "FileSuccessful",
              "nbObject": len(targetSEs)
          })
        else:
          gMonitor.addMark("PhysicalRemovalOK", len(targetSEs))
          gMonitor.addMark("PhysicalRemovalSize", opFile.Size * len(targetSEs))
>>>>>>> Migrate DMS/Agent/RequestOperations to ES.
        opFile.Status = "Done"

    if failed:
      self.operation.Error = "failed to remove %s files" % failed

    if self.rmsMonitoring:
      self.rmsMonitoringReporter.commit()

    return S_OK()

  def bulkRemoval(self, toRemoveDict, targetSE):
    """ bulk removal of lfns from :targetSE:

    :param dict toRemoveDict: { lfn : opFile, ... }
    :param str targetSE: target SE name
    """

    bulkRemoval = StorageElement(targetSE).removeFile(toRemoveDict)
    return bulkRemoval

  def singleRemoval(self, opFile, targetSE):
    """ remove single file from :targetSE: """
    proxyFile = None
    if "Write access not permitted for this credential" in opFile.Error:
      # # not a DataManger? set status to failed and return
      if "DataManager" not in self.shifter:
        opFile.Status = "Failed"
      elif not opFile.LFN:
        opFile.Error = "LFN not set"
        opFile.Status = "Failed"
      else:
        # #  you're a data manager - save current proxy and get a new one for LFN and retry
        saveProxy = os.environ["X509_USER_PROXY"]
        try:
          proxyFile = self.getProxyForLFN(opFile.LFN)
          if not proxyFile["OK"]:
            opFile.Error = proxyFile["Message"]
          else:
            proxyFile = proxyFile["Value"]
            removeFile = StorageElement(targetSE).removeFile(opFile.LFN)
            if not removeFile["OK"]:
              opFile.Error = removeFile["Message"]
            else:
              removeFile = removeFile["Value"]
              if opFile.LFN in removeFile["Failed"]:
                opFile.Error = removeFile["Failed"][opFile.LFN]
              else:
                # # reset error - replica has been removed this time
                opFile.Error = ""
        finally:
          if proxyFile:
            os.unlink(proxyFile)
          # # put back request owner proxy to env
          os.environ["X509_USER_PROXY"] = saveProxy
    return S_OK(opFile)
