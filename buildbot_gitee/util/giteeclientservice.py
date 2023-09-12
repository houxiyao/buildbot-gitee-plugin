from buildbot.util.httpclientservice import HTTPClientService
from buildbot.util.service import ReconfigurableServiceMixin
from twisted.application import service
from twisted.internet import defer


GITEE_API_BASE_URL = ""


class GiteeClientService(HTTPClientService):
    def __init__(self):
        super().__init__(GITEE_API_BASE_URL)

    @defer.inlineCallbacks
    def get_oauth2_token(self, username, password, client_id, client_secret, scope):
        res = yield self.post("https://gitee.com/oauth/token", data={
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope
        })
        res_json = yield res.json()
        if res.code not in (200, 201, 202):
            raise RuntimeError(res_json)
        return res_json
