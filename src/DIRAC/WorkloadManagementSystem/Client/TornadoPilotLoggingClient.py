from DIRAC.Core.Tornado.Client.TornadoClient import TornadoClient


class TornadoPilotLoggingClient(TornadoClient):
    """
    Tornado pilot logging client intended to be used when contacting TornadoPilotLogging service.
    """

    def getMetadata(self):
        """
        Get metadata from the server.

        :return: Dirac S_OK/S_ERROR dictionary with server properties.
        :rtype: dict
        """

        retVal = self.executeRPC("getMetadata")

        return retVal
