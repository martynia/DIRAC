"""
MeessageQueue Pilot logging plugin. Just log messages.
"""
import re
from DIRAC import S_OK, S_ERROR, gLogger

sLog = gLogger.getSubLogger(__name__)


class MQPilotLoggingPlugin:
    """
    A template of a MQ logging plugin.
    It gets the message and converts it to a list of Dictionaries to be shipped to a remote MQ service
    """

    def __init__(self):

        sLog.warning("MQPilotLoggingPlugin skeleton is being used. NO-op")
        self.rcompiled = re.compile(
            r"(?P<date>[0-9-]+)T(?P<time>[0-9:,]+)Z (?P<loglevel>DEBUG|INFO|ERROR|NOTICE) (?:\[(?P<source>[a-zA-Z]+)\] )?(?P<message>.*)"
        )

    def sendMessage(self, message, UUID):
        """
        A message could of a form:
        2022-06-10T11:02:02,823512Z DEBUG    [pilotLogger] X509_USER_PROXY=/scratch/dir_2313/user.proxy


        :param message: text to log
        :type message: str
        :return: None
        :rtype: None
        """

        res = self.rcompiled.match(message)
        if res:
            resDict = res.groupdict()
            # {'date': '2022-06-10', 'loglevel': 'DEBUG',
            # 'message': '   [pilotLogger] X509_USER_PROXY=/scratch/dir_2313/user.proxy',
            # 'time': '11:02:02,823512', 'source': None}
            return S_OK()
        else:
            return S_ERROR("No match - message could not be parsed")
