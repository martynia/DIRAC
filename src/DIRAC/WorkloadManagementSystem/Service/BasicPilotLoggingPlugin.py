"""
Basic Pilot logging plugin. Just log messages.
"""
from DIRAC import S_OK, S_ERROR, gLogger

sLog = gLogger.getSubLogger(__name__)


class BasicPilotLoggingPlugin:
    """
    This is a no-op fallback solution class, to be used when no plugin is defined for remote logging.
    Any pilot logger plugin could inherit from this class to receive a set of no-op methods required by
    :class:`TornadoPilotLoggingHandler` and only overwrite needed methods.
    """

    def __init__(self):

        sLog.warn("BasicPilotLoggingPlugin is being used. It only logs locally at a debug level.")

    def sendMessage(self, message, UUID, vo):
        """
        Dummy sendMessage method.

        :param str message: text to log
        :return: None
        :rtype: None
        """
        sLog.debug(message)
        return S_OK("Message sent")

    def finaliseLogs(self, payload, UUID, vo):
        """
        Dummy finaliseLogs method.

        :param payload:
        :type payload:
        :return: S_OK or S_ERROR
        :rtype: dict
        """

        return S_OK("Finaliser!")

    def getMeta(self):
        """
        Get metadata dummy method.

        :return: S_OK with an empty dict
        :rtype: dict
        """
        return S_OK({})
