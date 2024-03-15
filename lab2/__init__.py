from typing import Any


class Listener:
    def receive(self, msg: dict[Any, Any]) -> Any:
        print(f"Message from {msg['from']} to {self}: \n ------ {msg['message']}\n")

class Sender:
    def send(self, recipient: Listener, msg: Any) -> Any:
        recipient.receive({"from": self, "message": msg})
