from buildbot.secrets.providers.base import SecretProviderBase
from buildbot.secrets.providers.vault import HashiCorpVaultSecretProvider
from buildbot.util import httpclientservice, diffSets
from typing import List
from buildbot import config
from twisted.internet import defer
# curl -X POST --data-urlencode "grant_type=password" --data-urlencode "username={email}" --data-urlencode "password={password}" --data-urlencode "client_id={client_id}" --data-urlencode "client_secret={client_secret}" --data-urlencode "scope=projects user_info issues notes" https://gitee.com/oauth/token

SUPPORT_SCOPES = ["issues", "notes"]

class GiteeSecretInAHTTP(SecretProviderBase):
    name = "GiteeSecretInHTTP"

    def checkConfig(self, username=None, password=None, client_id=None, client_secret=None, scope=SUPPORT_SCOPES):
        if username is None:
            config.error("username 不能为空")
        if password is None:
            config.error("password 不能为空")
        if client_id is None:
            config.error("client_id 不能为空")
        if client_secret is None:
            config.error("client_secret 不能为空")
        if not isinstance(scope, list):
            config.error(f"scope 必须是一个字符串列表")

        _, unsupport_scopes = diffSets(SUPPORT_SCOPES, scope)
        if unsupport_scopes:
            config.error(f"scope 不支持 {unsupport_scopes}")

    @defer.inlineCallbacks
    def reconfigService(self, username=None, password=None, client_id=None, client_secret=None, scope=SUPPORT_SCOPES):
        self._http = yield httpclientservice.HTTPClientService.getService(
            self.master, self.vaultServer, headers={'X-Vault-Token': self.vaultToken})
        

    def startService(self):
        pass
