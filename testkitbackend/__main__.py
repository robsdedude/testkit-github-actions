from socketserver import TCPServer, StreamRequestHandler
from .dummy_backend import DummyBackend


class Server(TCPServer):
    allow_reuse_address = True

    def __init__(self, address):
        class Handler(StreamRequestHandler):
            def handle(self):
                print("Connected")
                backend = DummyBackend(self.rfile, self.wfile)
                while backend.process_request():
                    pass
                print("Disconnected")
        super(Server, self).__init__(address, Handler)


if __name__ == "__main__":
    server = Server(("0.0.0.0", 9876))

    print("Listening")
    while True:
        server.handle_request()
