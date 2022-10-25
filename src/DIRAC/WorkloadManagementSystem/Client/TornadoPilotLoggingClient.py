from DIRAC.Core.Base.Client import Client, createClient


@createClient("WorkloadManagement/TornadoPilotLogging")
class TornadoPilotLoggingClient(Client):
    def __init__(self, url=None, **kwargs):
        """
        Initialise a client.

        :param str url: Server URL, if None, defaults to "WorkloadManagement/TornadoPilotLogging"
        :param dict kwargs: additional keyword arguments, currently unused.
        """
        super(TornadoPilotLoggingClient, self).__init__(**kwargs)
        if not url:
            self.serverURL = "WorkloadManagement/TornadoPilotLogging"
        else:
            self.serverURL = url

    def getMetadata(self):
        """
        Get metadata from the server.

        :return: Dirac S_OK/S_ERROR dictionary with server properties.
        :rtype: dict
        """

        retVal = self._getRPC().getMetadata()

        return retVal
