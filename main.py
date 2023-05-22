import os
import hashlib

from frida_tools.application import ConsoleApplication
from frida_tools.tracer import UI

from utils import Request, Response, Message


class Agent:
    def __init__(self, session, reactor):
        self._script_path = './_agent.js'
        with open(self._script_path) as src_f:
            script_src = src_f.read()
        self._script = session.create_script(script_src)
        self._reactor = reactor
        self._agent = None
        self.requests = dict()
        self._plugin_dir = 'appData'

    def start_hooking(self, ui):
        def on_message(message, data):
            self._reactor.schedule(lambda: self._on_message(message, data))

        self._script.on('message', on_message)
        self._script.load()
        ui._update_status("Installing hooks...")
        self._agent = self._script.exports_sync
        self._agent.hook([], ['HTTPInterceptor'])
        ui._resume()

    def _on_message(self, msg, data):

        message = Message(msg, data)

        if "resume" in message.symbol:
            r = Request(*message.args)
            self.requests[hashlib.md5(message.args[0].encode()).hexdigest()] = r

            if message.data:
                r.set_body(message.data, self._plugin_dir)
        else:
            key = hashlib.md5(message.args[0].encode()).hexdigest()
            r = self.requests.get(key, None)
            if r:
                r.response = Response(*message.args)

                if "AWEJSONResponseSerializer" in message.symbol:
                    if message.ret:
                        r.response.set_body(message.ret.encode(), self._plugin_dir)
                elif "AWEBinaryResponseSerializer" in message.symbol:
                    if message.data:
                        r.response.set_body(message.data, self._plugin_dir)

                print(r)
                del self.requests[key]

        #print(self.requests, file=open("/tmp/requests.txt", "w"))


class TikTokHTTPInterceptor(ConsoleApplication, UI):
    def _usage(self):
        return "usage: python main.py [options] target"

    def _needs_target(self):
        return True

    def _start(self):
        if not os.path.exists('appData'):
            os.makedirs('appData')
            os.makedirs(os.path.join('appData', 'RequestBodies'))
            os.makedirs(os.path.join('appData', 'ResponseBodies'))
        agent = Agent(self._session, self._reactor)
        agent.start_hooking(self)


if __name__ == '__main__':
    TikTokHTTPInterceptor().run()
