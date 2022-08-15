"""
File cache logging plugin.
"""
import os, json, re
from DIRAC import S_OK, S_ERROR, gLogger

sLog = gLogger.getSubLogger(__name__)


class FileCacheLoggingPlugin:
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
        self.meta = {}
        logPath = os.path.join(os.getcwd(), "pilotlogs")
        self.meta["LogPath"] = logPath
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        sLog.info("Pilot logging directory:", logPath)

    def sendMessage(self, message, pilotUUID):
        """
        File cache sendMessage method. Write the log message to a file line by line.

        :param message: text to log in json format
        :type message: str
        :return: S_OK or S_ERROR
        :rtype: dict
        """

        res = self.pattern.match(pilotUUID)
        if not res:
            sLog.error("Pilot UUID does not match the UUID pattern: ", "%s" % (pilotUUID,))
            return S_ERROR("Pilot UUID is invalid")

        with open(os.path.join(self.meta["LogPath"], pilotUUID), "a") as pilotLog:
            try:
                messageContent = json.loads(message)
                if isinstance(messageContent, list):
                    for elem in messageContent:
                        pilotLog.write(elem + "\n")
                else:
                    # it could be a string, if emitted by pilot logger StringIO handler
                    pilotLog.write(messageContent)
            except IOError as ioerr:
                sLog.error("Error writing to log file:", str(ioerr))
                return S_ERROR(str(ioerr))
        return S_OK("Message logged successfully for pilot: %s" % (pilotUUID,))

    def finaliseLogs(self, payload, logfile):
        """
        Finalise a log file. Finalised logfile can be copied to a secure location.

        :param payload: additional info, a plugin might want to use (i.e. the system return code of a pilot script)
        :type payload: dict
        :param logfile: log filename (pilotUUID).
        :type logfile: json representation of dict
        :return: S_OK or S_ERROR
        :rtype: dict
        """

        returnCode = json.loads(payload).get("retCode", 0)
        res = self.pattern.match(logfile)
        if not res:
            sLog.error("Pilot UUID does not match the UUID pattern: ", "%s" % (logfile,))
            return S_ERROR("Pilot UUID is invalid")

        try:
            filepath = self.meta["LogPath"]
            os.rename(os.path.join(filepath, logfile), os.path.join(filepath, logfile + ".log"))
            sLog.info("Log file finalised for pilot: %s (return code: %s)" % (logfile, returnCode))
            return S_OK()
        except Exception as err:
            sLog.exception("Exception when finalising log: ", err)
            return S_ERROR(str(err))

    def getMeta(self):
        """
        Return any metadata related to this plugin. The "LogPath" is the minimum requirement for the dict to contain.

        :return: Dirac S_OK containing the metadata or S_ERROR if the LogPath is not defined.
        :rtype: dict
        """
        if "LogPath" in self.meta:
            return S_OK(self.meta)
        return S_ERROR("No Pilot logging directory defined")
