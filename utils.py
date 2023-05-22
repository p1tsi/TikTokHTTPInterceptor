import os
import json
from datetime import datetime

from time import time
from urllib.parse import urlparse


class Message(object):

    def __init__(self, message, data):
        self.timestamp = message['payload'].get('timestamp', '')
        self.tid = message['payload'].get('tid', '')
        self.plugin = message['payload'].get('type', '')
        self.symbol = message['payload'].get('symbol', '')

        func_data = message['payload'].get('data', {})
        self.args = func_data.get("args", [])
        self.ret = func_data.get("ret", "")
        self.data = data

    def __repr__(self):
        return f"{datetime.fromtimestamp((self.timestamp / 1000))} [{self.tid}] {self.plugin}:\t__CONTENT_TO_BE_PARSED__"


class Response:
    banner = "===== RESPONSE ====="

    def __init__(self, *args):
        self.url = args[0] or "N/A"
        self.status_code = args[1] or "N/A"
        self.headers = args[2] or "N/A"
        self.body = None

    def set_body(self, data, plugin_dir):
        if not self.body:
            filename = f"{urlparse(self.url).hostname}_{time()}"
            with open(os.path.join(plugin_dir, "ResponseBodies", filename), "wb") as body_fd:
                body_fd.write(data)
            # try:
            #    self.body = data.decode("utf8")
            # except:
            self.body = filename

    def _parse_headers(self):
        if self.headers:
            headers_str = "\n-- HEADERS --\n"
            headers = json.loads(self.headers)
            for header, value in headers.items():
                headers_str += f"{header}: {value}\n"
            return headers_str
        else:
            return ""

    def __repr__(self):
        response = f"\n{self.banner}\n{self.status_code}\n{self._parse_headers()}"

        if self.body:
            response += "\n-- BODY--\n"
            response += self.body
        response += "\n"
        return response


class Request:
    banner = "=============== REQUEST ==============="

    def __init__(self, *args):  # url=None, method=None, headers=None, body=None, cookies=None):
        self.url: str = args[0] or "N/A"
        self.method: str = args[1] or "N/A"
        self.headers: str = args[2] or None
        if len(args) > 3:
            self.cookies: str = args[3]
        else:
            self.cookies: str = ""
        self.body: str = ''
        self.response: Response = None

    def set_body(self, data, plugin_dir):
        if not self.body:
            filename = f"{urlparse(self.url).hostname}_{time()}"
            with open(os.path.join(plugin_dir, "RequestBodies", filename), "wb") as body_fd:
                body_fd.write(data)
            # try:
            #    self.body = data.decode("utf8")
            # except:
            self.body = filename

    def update_headers(self, new_headers):
        if new_headers:
            self.headers = new_headers

    def _headers_as_str(self):
        if self.headers:
            headers_str = "\n-- HEADERS --\n"
            try:
                headers = json.loads(self.headers)
                for header, value in headers.items():
                    headers_str += f"{header}: {value}\n"
            except:
                pass

            return headers_str
        else:
            return ""

    def _parse_cookies(self):
        if self.cookies:
            cookie_str = "\n-- COOKIES --\n"
            for cookie in self.cookies:
                cookie_str += f"{cookie}\n"
            return cookie_str
        else:
            return ""

    def __repr__(self):
        request = f"{self.banner}\n{self.method} {self.url}\n{self._headers_as_str()}{self._parse_cookies()}"

        if self.body:
            request += "\n-- BODY--\n"
            request += f"{self.body}\n"

        if self.response:
            request += str(self.response)

        return request

    def to_dict(self):
        request_as_dict = {'request': {}}
        request_as_dict['request']['url'] = self.url
        request_as_dict['request']['method'] = self.method
        request_as_dict['request']['headers'] = json.loads(self.headers) if self.headers else ""
        if self.cookies:
            request_as_dict['request']['cookies'] = self.cookies

        request_as_dict['request']['body'] = self.body

        return request_as_dict
