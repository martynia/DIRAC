"""
Test of multi-VO user metadata handling. Assumes a running Dirac instance with the (master?) FileCatalog
"""

import unittest
import os
import os.path

from DIRAC.Core.Base.Script import parseCommandLine

parseCommandLine()

from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC import gLogger
from DIRAC.Core.Utilities.Time import toString


def random_dd(outfile, size_mb):
    import os
    with open(outfile, 'w') as f:
        for i in range((int(size_mb) * 2 ** 20) / 512):
            f.write(os.urandom(512))


class TestUserMetadataTestCase(unittest.TestCase):
    def setUp(self):
        self.dirac = Dirac()

        self.lfn5 = '/gridpp/user/m/martynia/FC_test/test_file_10MB_v5.bin'
        self.dir5 = os.path.dirname(self.lfn5)
        # local file, for now:
        self.fullPath = 'test_file_10MB.bin'
        random_dd(self.fullPath, 10)
        diracSE = 'UKI-LT2-IC-HEP-disk'
        # add a replica
        result = self.dirac.addFile(self.lfn5, self.fullPath, diracSE)
        self.assertTrue(result['OK'])

    def tearDown(self):
        # meta index -r
        result = self.dirac.deleteMetadataField('JMMetaInt6')
        # delete a sole replica: dirac-dms-remove-files
        result = self.dirac.removeFile(self.lfn5)
        self.assertTrue(result['OK'])
        os.remove(self.fullPath)


class testMetadata(TestUserMetadataTestCase):
    def test_AddQueryRemove(self):
        result = self.dirac.getLfnMetadata(self.lfn5)
        self.assertTrue(result['OK'])
        self.assertTrue(self.lfn5 in result['Value']['Successful'].keys())
        self.assertEqual(result['Value']['Failed'], {})

        # meta index -f
        result = self.dirac.addMetadataField('JMMetaInt6', 'INT', metaType='-f')
        self.assertTrue(result['OK'])
        self.assertNotEqual(result['Value'], 'Already exists')
        self.assertTrue(result['Value'].startswith('Added new metadata:'))

        # meta index -d
        result = self.dirac.addMetadataField('JMTestDirectory6', 'INT', metaType='-d')
        self.assertTrue(result['OK'])
        self.assertNotEqual(result['Value'], 'Already exists')
        self.assertTrue(result['Value'].startswith('Added new metadata:'))

        # meta show
        result = self.dirac.getMetadataFields()
        self.assertTrue(result['OK'])
        self.assertDictContainsSubset({'JMMetaInt6': 'INT', }, result['Value']['FileMetaFields'])
        self.assertDictContainsSubset({'JMTestDirectory6': 'INT', }, result['Value']['DirectoryMetaFields'])

        # meta set
        metaDict6 = {'JMMetaInt6': 13}
        result = self.dirac.setMetadata(self.lfn5, metaDict6)
        self.assertTrue(result['OK'])

        metaDirDict6 = {'JMTestDirectory6': 126}
        result = self.dirac.setMetadata(self.dir5, metaDirDict6)
        self.assertTrue(result['OK'])

        # find
        result = self.dirac.findFilesByMetadata(metaDict6)
        self.assertTrue(result['OK'])
        self.assertIn(self.lfn5, result['Value'])

        # find
        metaDirDict = {'JMTestDirectory6': 126}
        result = self.dirac.findDirectoriesByMetadata(metaDirDict, path='/')
        self.assertTrue(result['OK'])
        self.assertIn(self.dir5, result['Value'].values())

        # API call only
        result = self.dirac.getFileUserMetadata(self.lfn5, printOutput=False)
        self.assertTrue(result['OK'])
        # 'Value': {'JMMetaInt6': 13L, 'JMMetaInt5': 12L, 'JMTestDirectory': 124L}
        self.assertDictContainsSubset({'JMMetaInt6': 13L}, result['Value'])
        # file: return  enclosing directory
        result = self.dirac.getDirectoryUserMetadata(self.lfn5)
        self.assertTrue(result['OK'])
        self.assertDictContainsSubset({'JMTestDirectory6': 126L}, result['Value'])
        # directory only
        result = self.dirac.getDirectoryUserMetadata(self.dir5)
        self.assertTrue(result['OK'])
        self.assertDictContainsSubset({'JMTestDirectory6': 126L}, result['Value'])
        # replicas
        # metaDict6={'JMMetaInt6':13}
        # result = self.dirac.getReplicasByMetadata(metaDict, path='/')
        # print result
        # self.assertTrue(result['OK'])

        # meta index -r
        result = self.dirac.deleteMetadataField('JMMetaInt6')
        self.assertTrue(result['OK'])

        result = self.dirac.deleteMetadataField('JMTestDirectory6')
        self.assertTrue(result['OK'])

    def test_ReplicasByMetadata(self):
        metaDict6={'JMMetaInt6':13}
        result = self.dirac.getReplicasByMetadata(metaDict6, path='/')
        self.assertTrue(result['OK'])

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUserMetadataTestCase)
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testMetadata))
    testResult = unittest.TextTestRunner(verbosity=2).run(suite)
