import sublime
import threading
import json
import urllib

from .helpers import get_settings


class ThreadUrl(threading.Thread):

    def __init__(self, url, callback, data, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.timeout = timeout
        self.callback = callback

    def run(self):
        response = urllib.request.urlopen(
            self.url, self.data, self.timeout)
        self.callback(response.read())


def async_urlopen(url, callback, data, timeout):
    thread = ThreadUrl(url, callback, data, timeout)
    thread.start()


def get_response(view, endpoint, callback, params=None, timeout=None):
    parameters = {}
    location = view.sel()[0]
    cursor = view.rowcol(location.begin())

    parameters['line'] = str(cursor[0] + 1)
    parameters['column'] = str(cursor[1] + 1)
    parameters['buffer'] = view.substr(sublime.Region(0, view.size()))
    parameters['filename'] = view.file_name()

    if params is not None:
        parameters.update(params)
    if timeout is None:
        timeout = int(get_settings(view, 'omnisharp_response_timeout'))

    host = get_settings(view, 'omnisharp_host')
    port = int(get_settings(view, 'omnisharp_port'))

    httpurl = "http://%s:%s/" % (host, port)

    target = urllib.parse.urljoin(httpurl, endpoint)
    data = urllib.parse.urlencode(parameters).encode('utf-8')

    async_urlopen(
        target,
        lambda jsonStr: callback(json.loads(jsonStr.decode('utf-8'))),
        data,
        timeout)
