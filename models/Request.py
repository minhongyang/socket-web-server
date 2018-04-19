import urllib.parse

from utils import log


class Request(object):
    def __init__(self):
        self.method = ''
        self.path = ''
        self.query = {}
        self.headers = {}
        self.body = {}
        self.cookies = {}

    def parsed_request(self, request):
        if request != '':
            head, body = request.split('\r\n\r\n', 1)

            h = head.split('\r\n')
            self.method = h[0].split()[0]

            path = h[0].split()[1]
            if path.find('?') != -1:
                self.path, q = path.split('?', 1)
                for item in q.split('&'):
                    k, v = item.split('=')
                    self.query[k] = v
            else:
                self.path = path

            for line in h[1:]:
                k, v = line.split(': ', 1)
                self.headers[k] = v

            if body != '':
                body = urllib.parse.unquote(body)
                for item in body.split('&'):
                    k, v = item.split('=')
                    self.body[k] = v

            cookie = self.headers.get('Cookie', '')
            for kv in cookie.split('; '):
                if kv.find('=') != -1:
                    k, v = kv.split('=')
                    self.cookies[k] = v

            log('parsed request\r\n', 'method:', self.method, '\r\npath:', self.path,
                '\r\nquery:', self.query, '\r\nheaders:', self.headers,
                '\r\nbody:', self.body, '\r\ncookies:', self.cookies
                )
        else:
            log('Browser just sent an empty request!')
