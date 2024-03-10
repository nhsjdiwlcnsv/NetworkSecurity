class Listener:
    def receive(self, msg: str) -> ...:
        ...

class Sender:
    def send(self, recipient: Listener, msg: str) -> None:
        recipient.receive(msg)
