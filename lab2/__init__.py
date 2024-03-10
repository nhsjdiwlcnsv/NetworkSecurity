from typing import Any


class Listener:
    def receive(self, msg: Any) -> ...:
        ...

class Sender:
    def send(self, recipient: Listener, msg: Any) -> None:
        recipient.receive(msg)
