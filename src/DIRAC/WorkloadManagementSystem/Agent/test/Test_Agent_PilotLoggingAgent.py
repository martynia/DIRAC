import unittest
import os
from contextlib import contextmanager
from unittest.mock import MagicMock, patch, call

from DIRAC import gLogger, gConfig, S_OK, S_ERROR
import DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent
from DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent import PilotLoggingAgent


@contextmanager
def patch_parent(class_):
    """
    Mock the bases.
    source: https://stackoverflow.com/a/24577389/9893423
    """
    yield type(class_.__name__, (MagicMock,), dict(class_.__dict__))


class PilotLoggingAgentTestCase(unittest.TestCase):
    def setUp(self):
        pass

        self.maxDiff = None

    def tearDown(self):
        pass

    @patch.object(
        DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent,
        "getVOs",
        return_value={"OK": True, "Value": ["gridpp, lz"]},
    )
    @patch.object(DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.gConfig, "getValue", return_value="GridPP")
    def test_initialize(self, mockSetup, mockVOs):
        with patch_parent(PilotLoggingAgent) as MockAgent:
            mAgent = MockAgent()
            res = mAgent.initialize()
            self.assertEqual(mAgent.voList, mockVOs.return_value["Value"])
            self.assertIsNotNone(mAgent.setup)
            self.assertEqual(res, S_OK())

    @patch("DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.Operations")
    @patch.object(
        DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent,
        "getVOs",
        return_value={"OK": True, "Value": ["gridpp"]},
    )
    @patch.object(DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.gConfig, "getValue", return_value="GridPP")
    @patch.object(
        DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.PilotLoggingAgent, "executeForVO", return_value=S_OK()
    )
    def test_execute(self, mockExVO, mockSetup, mockVOs, mockOp):
        with patch_parent(PilotLoggingAgent) as MockAgent:
            mAgent = MockAgent()
            res = mAgent.initialize()
            self.assertEqual(res, S_OK())
            self.assertEqual(mAgent.voList, mockVOs.return_value["Value"])
            self.assertEqual(mAgent.setup, mockSetup.return_value)
            # pilot logging on:
            mockOp.return_value.getValue.return_value = True
            # proxy user and group:
            upDict = {
                "OK": True,
                "Value": {"User": "proxyUser", "Group": "proxyGroup"},
            }
            mockOp.return_value.getOptionsDict.return_value = upDict
            vo = mockVOs.return_value["Value"][0]
            res = mAgent.execute()
            assert mockOp.called
            mockOp.assert_called_with(vo=vo, setup=mockSetup.return_value)
            mockOp.return_value.getValue.assert_called_with("/Pilot/RemoteLogging", True)
            mockOp.return_value.getOptionsDict.assert_called_with("Shifter/DataManager")
            mAgent.executeForVO.assert_called_with(
                vo,
                proxyUserName=upDict["Value"]["User"],
                proxyUserGroup=upDict["Value"]["Group"],
            )
            self.assertEqual(res, S_OK())

            # pilot logger off, skip the VO:
            mockOp.return_value.getValue.return_value = False
            res = mAgent.execute()
            self.assertEqual(res, S_OK())

            # pilot logger on, no user/group dict
            mockOp.return_value.getValue.return_value = True
            mockOp.return_value.getOptionsDict.return_value = {"OK": False}
            res = mAgent.execute()
            self.assertEqual(res["OK"], False)
            self.assertEqual(res["Message"], "Agent cycle for some VO finished with errors")
            self.assertIn(vo, res)
            self.assertEqual(res[vo], "No shifter defined - skipped")

            # pilot logger on, no user or group defined
            for key in ["User", "Group"]:
                mockOp.return_value.getValue.return_value = True
                mockOp.return_value.getOptionsDict.return_value = {"OK": True, "Value": {key: "someValue"}}
                res = mAgent.execute()
                self.assertEqual(res["OK"], False)
                self.assertIn(vo, res)
                self.assertIsNotNone(res[vo])

    @patch("DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.Operations")
    @patch("DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.DataManager")
    @patch.object(DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.os, "listdir")
    @patch.object(DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.os, "remove")
    @patch.object(DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.os.path, "isfile")
    @patch.object(DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.os.path, "exists")
    @patch("DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent.TornadoPilotLoggingClient")
    @patch.object(DIRAC.WorkloadManagementSystem.Agent.PilotLoggingAgent, "executeWithUserProxy")
    def test_executeForVO(self, mockProxy, mockTC, mockexists, mockisfile, mockremove, mocklistdir, mockDM, mockOp):
        with patch_parent(PilotLoggingAgent) as MockAgent:

            opsHelperValues = {"UploadSE": "testUploadSE", "UploadPath": "/gridpp/uploadPath"}
            mAgent = MockAgent()
            mockOp.return_value.getOptionsDict.return_value = opsHelperValues
            mAgent.opsHelper = mockOp.return_value
            mockisfile.return_value = True
            mocklistdir.return_value = ["file1.log", "file2.log", "file3.log"]
            resDict = {"OK": True, "Value": {"LogPath": "/pilot/log/path/"}}
            mockTC.return_value.getMetadata.return_value = resDict
            vo = "gridpp"

            # success route
            res = mAgent.executeForVO(vo=vo)

            mockTC.assert_called_with(useCertificates=True)
            assert mockTC.return_value.getMetadata.called
            mockexists.return_value = True
            mocklistdir.assert_called_with(os.path.join(resDict["Value"]["LogPath"], vo))

            calls = []
            for elem in mocklistdir.return_value:
                calls.append(call(os.path.join(resDict["Value"]["LogPath"], vo, elem)))
            mockisfile.assert_has_calls(calls)

            assert mockDM.called
            mockDM.return_value.putAndRegister.return_value = {"OK": True}

            calls = []
            mockDM.return_value.putAndRegister.assert_called()
            for elem in mocklistdir.return_value:
                lfn = os.path.join(opsHelperValues["UploadPath"], elem)
                name = os.path.join(resDict["Value"]["LogPath"], vo, elem)
                mockDM.return_value.putAndRegister.assert_any_call(
                    lfn=lfn, fileName=name, diracSE=opsHelperValues["UploadSE"], overwrite=True
                )

            call_count = len(mocklistdir.return_value)
            self.assertEqual(call_count, mockDM.return_value.putAndRegister.call_count)
            self.assertEqual(call_count, mockremove.call_count)
            # and finally:
            self.assertTrue(res["OK"])

            # failure routes, test in the reverse order for convenience
            # getMetadata() call failed
            mAgent = MockAgent()
            mAgent.opsHelper.getValue.side_effect = opsHelperValues
            mockTC.reset_mock(return_value=True)
            mockTC.return_value.getMetadata.return_value = {"OK": False, "Message": "Failed, sorry.."}
            res = mAgent.executeForVO(vo=vo)
            self.assertFalse(res["OK"])

            # config values not correct:
            opsHelperValues = [None, "/uploadPath", "tornadoServer"]
            mAgent.opsHelper.getValue.side_effect = opsHelperValues
            res = mAgent.executeForVO(vo=vo)
            self.assertFalse(res["OK"])

            opsHelperValues = ["uploadSE", None, "tornadoServer"]
            mAgent.opsHelper.getValue.side_effect = opsHelperValues
            res = mAgent.executeForVO(vo=vo)
            self.assertFalse(res["OK"])

            opsHelperValues = ["uploadSE", "uploadPath", None]
            mAgent.opsHelper.getValue.side_effect = opsHelperValues
            res = mAgent.executeForVO(vo=vo)
            self.assertFalse(res["OK"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PilotLoggingAgentTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
