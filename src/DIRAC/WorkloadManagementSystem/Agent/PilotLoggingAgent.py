""" :mod: PilotLoggingAgent

    PilotLoggingAgent sends Pilot log files to an SE
"""

# # imports
import os
from DIRAC import S_OK, S_ERROR, gConfig
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.WorkloadManagementSystem.Client.TornadoPilotLoggingClient import TornadoPilotLoggingClient
from DIRAC.ConfigurationSystem.Client.Helpers.Registry import getVOs
from DIRAC.Core.Utilities.Proxy import executeWithUserProxy


class PilotLoggingAgent(AgentModule):
    """
    .. class:: PilotLoggingAgent

    The agent sends completed pilot log files to permanent storage for analysis.
    """

    def initialize(self):
        """
        agent's initalisation. Use this agent's CS information to:
        Determine what Defaults/Shifter shifter proxy to use.,
        get the target SE name from the CS.
        Obtain log file location from Tornado.

        :param self: self reference
        """

        # configured VOs and setup
        res = getVOs()
        if res["OK"]:
            self.voList = res.get("Value", [])
        else:
            return S_ERROR(res["Message"])

        if isinstance(self.voList, str):
            self.voList = [self.voList]

        self.setup = gConfig.getValue("/DIRAC/Setup", None)
        if self.setup is None:
            self.log.error("Setup is not defined in the configuration")
            return S_ERROR("Setup is not defined in the configuration")

        return S_OK()

    def execute(self):
        """
        Execute one agent cycle. Upload log files to the SE and register them in the DFC.
        Use a shifter proxy dynamically loaded for every VO

        :param self: self reference
        """
        voRes = {}
        for vo in self.voList:
            self.opsHelper = Operations(vo=vo, setup=self.setup)
            # is remote pilot logging enabled for the VO ?
            pilotLogging = self.opsHelper.getValue("/Pilot/RemoteLogging", True)
            if pilotLogging:
                res = self.opsHelper.getOptionsDict("/Shifter/DataManager")
                if not res["OK"]:
                    voRes[vo] = "No shifter defined - skipped"
                    self.log.error(f"No shifter defined for VO: {vo} - skipping ...")
                    continue

                proxyUser = res["Value"].get("User", None)
                proxyGroup = res["Value"].get("Group", None)
                if proxyGroup is None or proxyUser is None:
                    self.log.error(
                        f"No proxy user or group defined for pilot: VO: {vo}, User: {proxyUser}, Group: {proxyGroup}"
                    )
                    voRes[vo] = "No proxy user or group defined - skipped"
                    continue

                self.log.info(f"Proxy used for pilot logging: VO: {vo}, User: {proxyUser}, Group: {proxyGroup}")
                res = self.executeForVO(vo, proxyUserName=proxyUser, proxyUserGroup=proxyGroup)
                if not res["OK"]:
                    voRes[vo] = res["Message"]
        if voRes:
            voRes.update(S_ERROR("Agent cycle for some VO finished with errors"))
            return voRes
        return S_OK()

    @executeWithUserProxy
    def executeForVO(self, vo):
        """
        Execute one agent cycle for VO

        :param vo: vo enabled for remote pilot logging
        :type vo: str
        :return: S_OK or S_ERROR
        :rtype: dict
        """

        self.log.info(f"Pilot files upload cycle started for VO: {vo}")
        uploadSE = self.opsHelper.getValue("/Pilot/UploadSE")
        if uploadSE is None:
            return S_ERROR("Upload SE not defined")
        self.log.info(f"Pilot upload SE: {uploadSE}")

        uploadPath = self.opsHelper.getValue("/Pilot/UploadPath")
        if uploadPath is None:
            return S_ERROR(f"Upload path on SE {uploadSE} not defined")
        uploadPath = os.path.join("/", vo, uploadPath)
        self.log.info(f"Pilot upload path: {uploadPath}")

        server = self.opsHelper.getValue("/Pilot/RemoteLoggerURL")

        if server is None:
            return S_ERROR(f"No DownloadLocation (server) set in the CS for VO: {vo}!")
        client = TornadoPilotLoggingClient(server, useCertificates=True)
        resDict = client.getMetadata()

        if not resDict["OK"]:
            return S_ERROR(resDict["Message"])
        pilotLogPath = resDict["Value"]["LogPath"]
        self.log.info(f"Pilot log files location = {pilotLogPath} for VO: {vo}")

        # get finalised (.log) files from Tornado and upload them to the selected SE

        files = [
            f for f in os.listdir(pilotLogPath) if os.path.isfile(os.path.join(pilotLogPath, f)) and f.endswith("log")
        ]

        if not files:
            self.log.info("No files to upload for this cycle")
        for elem in files:
            lfn = os.path.join(uploadPath, elem)
            name = os.path.join(pilotLogPath, elem)
            res = DataManager().putAndRegister(lfn=lfn, fileName=name, diracSE=uploadSE, overwrite=True)
            if not res["OK"]:
                self.log.error("Could not upload", f"to {uploadSE}: {res['Message']}")
            else:
                self.log.info("File uploaded: ", f"LFN = {res['Value']}")
                try:
                    os.remove(name)
                except Exception as excp:
                    self.log.exception("Cannot remove a local file after uploading", lException=excp)
        return S_OK()
