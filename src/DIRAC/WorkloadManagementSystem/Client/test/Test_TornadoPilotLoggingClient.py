import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

import DIRAC.WorkloadManagementSystem.Client.TornadoPilotLoggingClient as tplc


class TestTornadoPilotLoggingClient(unittest.TestCase):
    @patch.object(tplc.TornadoPilotLoggingClient, "executeRPC", return_value={"key": "value"})
    def test_client(self, clientMock):
        client = tplc.TornadoPilotLoggingClient("test.server", useCertificates=True)
        res = client.getMetadata()
        clientMock.assert_called_with("getMetadata")
        self.assertEqual(res, clientMock.return_value)


if __name__ == "__main__":
    unittest.main()
