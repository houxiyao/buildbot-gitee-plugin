from twisted.internet import defer
from twisted.python.filepath import FilePath
from twisted.trial import unittest

from buildbot.secrets.providers.file import SecretInAFile
from buildbot.test.util.config import ConfigErrorsMixin
from buildbot.util.misc import writeLocalFile


class TestSecretInFile(ConfigErrorsMixin, unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        self.tmp_dir = self.createTempDir("temp")
        self.filepath = self.createFileTemp(self.tmp_dir, "tempfile.txt",
                                            text="key value\n")
        self.srvfile = SecretInAFile(self.tmp_dir)
        yield self.srvfile.startService()

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.srvfile.stopService()
