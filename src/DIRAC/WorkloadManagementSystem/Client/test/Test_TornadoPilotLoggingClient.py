import unittest
from unittest.mock import patch

from DIRAC.WorkloadManagementSystem.Client.TornadoPilotLoggingClient import TornadoPilotLoggingClient


class TestTornadoPilotLoggingClient(unittest.TestCase):
    @patch("TornadoClient")
    def test_client(self, clientMock):
        client = TornadoPilotLoggingClient("test.server", useCertificates=True)
        client.getMetadata()
        clientMock.executeRPC.assert_called()


if __name__ == "__main__":
    unittest.main()
