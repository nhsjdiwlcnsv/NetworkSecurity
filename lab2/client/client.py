from typing import Any
from lab2 import Listener, Sender
from lab2.servers import Server


class Client(Listener, Sender):
    def __init__(self, key: str):
        self.__key = key

    def send(self, recipient: Server, msg: Any) -> None:
        recipient.receive(msg)

    def receive(self, msg: str) -> None:
        print(msg)

    @property
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, new_key: str) -> None:
        raise AttributeError("Cannot assign new key to the user!")

    @property
    def intkey(self) -> int:
        return sum(map(lambda x: ord(x), self.key))
