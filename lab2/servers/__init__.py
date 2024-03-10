import os
from typing import Any
from lab2 import Listener, Sender


class Server(Listener, Sender):
    def __init__(self, server_id: int):
        super().__init__()

        self._server_id: int = server_id
        self.received_data: Any = ""

    @property
    def server_id(self) -> int:
        return self._server_id

    def keygen(self) -> str:
        return os.urandom(8).hex().upper()

    def receive(self, msg: Any) -> None:
        self.received_data = msg
