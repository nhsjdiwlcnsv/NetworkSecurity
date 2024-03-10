from lab2 import Listener, Sender


class Server(Listener, Sender):
    def __init__(self, server_id: int):
        super().__init__()

        self._server_id: int = server_id
        self.received_data: str = ""

    def receive(self, msg: str) -> None:
        self.received_data = msg

    def _encrypt(self, msg: str) -> str:
        return msg
