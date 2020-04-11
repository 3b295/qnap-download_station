import requests

from typing import BinaryIO, Union
from base64 import b64encode


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class DownloadStation:
    PROTOCOL = 'http'
    APP_NAME = 'downloadstation'
    API_VERSION = 'V4'

    ERROR_CODE = {
        8196: 'duplicate',
        4097: 'not found',
    }

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.sid = None
        self.session = requests.Session()

    def get_sid(self):
        if not self.sid:
            self.sid = self.sid = self.misc_login({
                "user": self.username,
                "pass": b64encode(self.password.encode('ascii')).decode('ascii')
            })['sid']

        return self.sid

    def misc_login(self, params=None):
        """otherwise `get_sid` is called"""
        if params is None:
            params = {}

        return self._despatch_query(self._uri_for_path('misc', 'login'), params=params)

    def _uri_for_path(self, app, endpoint):
        app = ''.join(x.capitalize() for x in app.split('_'))
        endpoint = ''.join(x.capitalize() for x in endpoint.split('_'))

        return f"{self.PROTOCOL}://{self.host}/{self.APP_NAME}/{self.API_VERSION}/{app}/{endpoint}"

    def _despatch_query(self, uri, params=None, files=None):
        response = self.session.post(uri, data=params, files=files)
        if response.status_code != 200:
            raise ServerError(f'request err. status: {response.status_code}')

        json_body = response.json()

        error_code = json_body['error']
        if error_code:
            if error_code in self.ERROR_CODE:
                raise RequestError(
                    f'{error_code}({self.ERROR_CODE[error_code]}) {json_body["reason"]}')
            raise RequestError(f'{error_code} {json_body["reason"]}')

        return DotDict(json_body)

    def _handle(self, group, task, params=None, files=None):
        if params is None:
            params = {}

        return self._despatch_query(
            self._uri_for_path(group, task), dict(params, sid=self.get_sid()), files)

    def account_add(self, **extra):
        return self._handle('account', 'add', params=extra)

    def account_query(self, **extra):
        return self._handle('account', 'query', params=extra)

    def account_update(self, **extra):
        return self._handle('account', 'update', params=extra)

    def account_remove(self, **extra):
        return self._handle('account', 'remove', params=extra)

    def addon_query(self, **extra):
        return self._handle('addon', 'query', params=extra)

    def addon_enable(self, **extra):
        return self._handle('addon', 'enable', params=extra)

    def addon_verify(self, **extra):
        return self._handle('addon', 'verify', params=extra)

    def addon_install(self, **extra):
        return self._handle('addon', 'install', params=extra)

    def addon_uninstall(self, **extra):
        return self._handle('addon', 'uninstall', params=extra)

    def addon_search(self, **extra):
        return self._handle('addon', 'search', params=extra)

    def config_get(self, **extra):
        return self._handle('config', 'get', params=extra)

    def config_set(self, **extra):
        return self._handle('config', 'set', params=extra)

    def misc_dir(self, **extra):
        return self._handle('misc', 'dir', params=extra)

    def misc_env(self, **extra):
        return self._handle('misc', 'env', params=extra)

    def misc_logout(self, **extra):
        return self._handle('misc', 'logout', params=extra)

    def misc_socks_5(self, **extra):
        return self._handle('misc', 'socks_5', params=extra)

    def rss_add(self, **extra):
        return self._handle('rss', 'add', params=extra)

    def rss_query(self, **extra):
        return self._handle('rss', 'query', params=extra)

    def rss_update(self, **extra):
        return self._handle('rss', 'update', params=extra)

    def rss_remove(self, **extra):
        return self._handle('rss', 'remove', params=extra)

    def rss_query_feed(self, **extra):
        return self._handle('rss', 'query_feed', params=extra)

    def rss_update_feed(self, **extra):
        return self._handle('rss', 'update_feed', params=extra)

    def rss_add_job(self, **extra):
        return self._handle('rss', 'add_job', params=extra)

    def rss_update_job(self, **extra):
        return self._handle('rss', 'update_job', params=extra)

    def rss_remove_job(self, **extra):
        return self._handle('rss', 'remove_job', params=extra)

    def task_status(self, **extra):
        return self._handle('task', 'status', params=extra)

    def task_query(self, _from=None, limit=65536, field=None, reverse=True, **extra):
        direction = 'AES' if reverse else 'DESC'

        if field is None:
            direction = None

        return self._handle('task', 'query', params=dict({
            'form': _from,
            'limit': limit,
            'field': field,
            'direction': direction,
        }, **extra))

    def task_detail(self, **extra):
        return self._handle('task', 'detail', params=extra)

    def task_add_url(self, url: str, move: str, temp: str = None, **extra):
        if temp is None:
            temp = move

        return self._handle('task', 'add_url', params=dict({
            'url': url,
            'temp': temp,
            'move': move,
        }, **extra))

    def task_add_torrent(self, file: Union[BinaryIO, str], move: str, temp: str = None, **extra):
        if temp is None:
            temp = move

        need_close = False

        try:
            if isinstance(file, str):
                file = open(file, 'rb')
                need_close = True

            files = {
                'file[]': file,
            }

            return self._handle(
                'task', 'add_torrent',
                params=dict({
                    'temp': temp,
                    'move': move,
                }, **extra),
                files=files)
        finally:
            if need_close:
                file.close()

    def task_start(self, _hash: str, **extra):
        return self._handle('task', 'start', params=dict({'hash': _hash}, **extra))

    def task_stop(self, _hash: str, **extra):
        return self._handle('task', 'stop', params=dict({'hash': _hash}, **extra))

    def task_pause(self, _hash, **extra):
        return self._handle('task', 'pause', params=dict({'hash': _hash}, **extra))

    def task_remove(self, _hash, **extra):
        return self._handle('task', 'remove', params=dict({'hash': _hash}, **extra))

    def task_priority(self, **extra):
        return self._handle('task', 'priority', params=extra)

    def task_get_file(self, _hash: str, **extra):
        return self._handle('task', 'get_file', params=dict({'hash': _hash}, **extra))

    def task_set_file(self, **extra):
        return self._handle('task', 'set_file', params=extra)

    def task_get_torrent_file(self, **extra):
        return self._handle('task', 'get_torrent_file', params=extra)


class ServerError(Exception):
    """from download station server"""
    pass


class RequestError(Exception):
    """requests params error"""
    pass
