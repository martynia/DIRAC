""" Tornado-based HTTPs JobMonitoring service.
"""

import os
from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.ConfigurationSystem.Client.Helpers import Registry
from DIRAC.Core.Tornado.Server.TornadoService import TornadoService
from DIRAC.Core.DISET.RequestHandler import RequestHandler, getServiceOption
from DIRAC.Core.Utilities.ObjectLoader import ObjectLoader

sLog = gLogger.getSubLogger(__name__)


class TornadoPilotLoggingHandler(TornadoService):
    log = sLog

    @classmethod
    def initializeHandler(cls, infoDict):
        """
        Called once, at the first request. Create a directory where pilot logs will be stored.

        :param infoDict:
        :return: None
        """

        cls.log.info("Handler initialised ...")
        cls.log.debug("with a dict: ", str(infoDict))
        defaultOption, defaultClass = "LoggingPlugin", "BasicPilotLoggingPlugin"
        configValue = getServiceOption(infoDict, defaultOption, defaultClass)

        result = ObjectLoader().loadObject("WorkloadManagementSystem.Service.%s" % (configValue,), configValue)
        if not result["OK"]:
            cls.log.error("Failed to load LoggingPlugin", "%s: %s" % (configValue, result["Message"]))
            return result

        componentClass = result["Value"]
        cls.loggingPlugin = componentClass()
        cls.log.info("Loaded: PilotLoggingPlugin class", configValue)

        cls.meta = {}
        logPath = os.path.join(os.getcwd(), "pilotlogs")
        cls.meta["LogPath"] = logPath
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        cls.log.info("Pilot logging directory:", logPath)

    def initializeRequest(self):
        """
        Called for each request.

        :return: None
        """

        self.log.info("Request initialised.. ")

    auth_sendMessage = ["Operator", "Pilot", "GenericPilot"]

    def export_sendMessage(self, message, pilotUUID):
        # def export_sendMessage(self, message, pilotUUID):
        """
        The method logs messages to Tornado and forwards pilot log files, one per pilot, to a relevant plugin.
        The pilot is identified by its UUID.

        :param message: message sent by a client, a list of strings in JSON format
        :param pilotUUID: pilot UUID
        :return: S_OK or S_ERROR if a plugin cannot process the message.
        :rtype: dict
        """
        ## Insert your method here, don't forget the return should be serializable
        ## Returned value may be an S_OK/S_ERROR
        ## You don't need to serialize in JSON, Tornado will do it

        # determine client VO
        vo = self.__getClientVO()
        # the plugin returns S_OK or S_ERROR
        # leave JSON decoding to the selected plugin:
        result = self.loggingPlugin.sendMessage(message, pilotUUID, vo)
        return result

    auth_getMetadata = ["Operator", "TrustedHost"]

    def export_getMetadata(self):
        """
        Get PilotLoggingHandler metadata. Intended to be used by a client or an agent.

        :return: S_OK containing a metadata dictionary
        """
        return self.loggingPlugin.getMeta()

    auth_finaliseLogs = ["Operator", "Pilot", "GenericPilot"]

    def export_finaliseLogs(self, payload, pilotUUID):
        """
        Finalise a log file. Finalised logfile can be copied to a secure location, if a file cache is used.

        :param payload: data passed to the plugin finaliser.
        :type payload: dict
        :param pilotUUID: pilot UUID
        :return: S_OK or S_ERROR (via the plugin involved)
        :rtype: dict
        """

        vo = self.__getClientVO()

        # The plugin returns the Dirac S_OK or S_ERROR object
        return self.loggingPlugin.finaliseLogs(payload, pilotUUID, vo)

    def __getClientVO(self):
        # get client credentials to determine the VO
        credDict = self.getRemoteCredentials()
        pilotGroup = credDict["group"]
        return Registry.getVOForGroup(pilotGroup)
