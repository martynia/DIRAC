"""
File cache logging plugin.
"""
import os
import json
import re
import time
from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.WorkloadManagementSystem.Client.PilotLoggingPlugins.PilotLoggingPlugin import PilotLoggingPlugin

sLog = gLogger.getSubLogger(__name__)


class FileCacheLoggingPlugin(PilotLoggingPlugin):
    """
    File cache logging. Log records are appended to a file, one for each pilot.
    It is assumed that an agent will be installed together with this plugin, which will copy
    the files to a safe place and clear the cache.
    """

    def __init__(self):
        """
        Sets the pilot log files location for a WebServer.

        """
        # UUID pattern
        self.pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
        # pilot stamp pattern
        self.stamppattern = re.compile(r"^[0-9a-f]{32}$")
        self._logPath = os.path.join(os.getcwd(), "pilotlogs")
        if not os.path.exists(self._logPath):
            os.makedirs(self._logPath)
        sLog.verbose("Pilot logging directory:", self._logPath)

    def sendMessage(self, message, pilotUUID, vo):
        """
        File cache sendMessage method. Write the log message to a file line by line.

        :param str message: text to log in json format
        :param str pilotUUID: pilot id. Optimally it should be a pilot stamp if available, otherwise a generated UUID.
        :param str vo: VO name of a pilot which sent the message.
        :return: S_OK or S_ERROR
        :rtype: dict
        """

        if not self._verifyUUIDPattern(pilotUUID):
            return S_ERROR("Pilot UUID is invalid")

        dirname = os.path.join(self._logPath, vo)
        try:
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            with open(os.path.join(dirname, pilotUUID), "a") as pilotLog:
                try:
                    messageContent = json.loads(message)
                    if isinstance(messageContent, list):
                        for elem in messageContent:
                            pilotLog.write(elem + "\n")
                    else:
                        # it could be a string, if emitted by pilot logger StringIO handler
                        pilotLog.write(messageContent)
                except OSError as oserr:
                    sLog.error("Error writing to log file:", repr(oserr))
                    return S_ERROR(repr(oserr))
        except OSError as err:
            sLog.exception("Error opening a pilot log file", lException=err)
            return S_ERROR(repr(err))
        return S_OK(f"Message logged successfully for pilot: {pilotUUID} and {vo}")

    def finaliseLogs(self, payload, logfile, vo):
        """
        Finalise a log file. Finalised logfile can be copied to a secure location.

        :param dict payload: additional info, a plugin might want to use (i.e. the system return code of a pilot script)
        :param str logfile: log filename (pilotUUID).
        :param str vo: VO name of a pilot which sent the message.
        :return: S_OK or S_ERROR
        :rtype: dict
        """

        returnCode = json.loads(payload).get("retCode", 0)

        if not self._verifyUUIDPattern(logfile):
            return S_ERROR("Pilot UUID is invalid")

        try:
            filepath = self._logPath
            os.rename(os.path.join(filepath, vo, logfile), os.path.join(filepath, vo, logfile + ".log"))
            sLog.info(f"Log file {logfile} finalised for pilot: (return code: {returnCode})")
            return S_OK()
        except Exception as err:
            sLog.exception("Exception when finalising log")
            return S_ERROR(repr(err))

    def getLogs(self, vo):
        """
        Get all pilot logs for a VO from Tornado log storage area.

        :param str vo:
        :type vo:
        :return: Dirac S_OK containing the logs or S_ERROR
        :rtype: dict
        """
        topdir = os.path.join(self._logPath, vo)
        resultDict = {"Successful": {}, "Failed": {}}
        files = [f for f in os.listdir(topdir) if os.path.isfile(os.path.join(topdir, f)) and f.endswith("log")]
        for logfile in files:
            try:
                with open(os.path.join(topdir, logfile)) as lf:
                    stdout = lf.read()
                    resultDict["Successful"].update({logfile: stdout})
            except FileNotFoundError as err:
                sLog.error(f"Error opening a log file:{logfile}", err)
                resultDict["Failed"].update({logfile: repr(err)})

        return S_OK(resultDict)

    def deleteLogs(self, filelist, vo):
        """
        Delete log files from the server cache.
        :param list filelist: list of pilot log files to be deleted
        :param str vo: VO name
        :return: Dirac S_OK
        :rtype: dict
        """

        for elem in filelist:
            fullpath = os.path.join(self._logPath, vo, elem)
            sLog.debug(f" Deleting pilot log : {fullpath}")
            try:
                os.remove(fullpath)
            except Exception as excp:
                sLog.exception(f"Cannot remove a log file {fullpath}", lException=excp)
        return S_OK()

    def clearLogs(self, clearPilotsDelay, vo):
        """
        Delete old pilot log files if older that clearPilotsDelay days

        :param int pilotLogPath: maximum file age.
        :return: None
        :rtype: None
        """

        seconds = int(clearPilotsDelay) * 86400
        currentTime = time.time()
        files = os.listdir(os.path.join(self._logPath, vo))
        for elem in files:
            fullpath = os.path.join(self._logPath, vo, elem)
            modifTime = os.stat(fullpath).st_mtime
            if modifTime < currentTime - seconds:
                self.log.debug(f" Deleting old log : {fullpath}")
                try:
                    os.remove(fullpath)
                except Exception as excp:
                    self.log.exception(f"Cannot remove an old log file after {fullpath}", lException=excp)
        return S_OK()

    def getLog(self, logfile, vo):
        """
        Get the "instant" pilot logs from Tornado log storage area. There are not finalised (incomplete) logs.

        :return:  Dirac S_OK containing the logs
        :rtype: dict
        """

        filename = os.path.join(self._logPath, vo, logfile)
        resultDict = {}
        try:
            with open(filename) as f:
                stdout = f.read()
                resultDict["StdOut"] = stdout
        except FileNotFoundError as err:
            sLog.error(f"Error opening a log file:{filename}", err)
            return S_ERROR(repr(err))

        return S_OK(resultDict)

    def _verifyUUIDPattern(self, logfile):
        """
        Verify if the name of the log file matches the required pattern.

        :param str name: file name
        :return: re.match result
        :rtype: re.Match object or None.
        """

        res = self.stamppattern.match(logfile)
        if not res:
            res = self.pattern.match(logfile)
        if not res:
            sLog.error(
                "Pilot UUID does not match the UUID nor the stamp pattern. ",
                f"UUID: {logfile}, pilot stamp pattern {self.stamppattern}, UUID pattern {self.pattern}",
            )
        return res
