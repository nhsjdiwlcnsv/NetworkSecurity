from typing import Any

from lab2 import Sender
from lab2.servers import Server
from lab2.servers.kerberos import TicketGrantingServer
from lab2.utils.crypto import encrypt, decrypt
from lab2.utils.helpers import hex2decimal


class ServiceServer(Server):
    def __init__(self, server_id: int):
        super().__init__(server_id)

    def receive(self, msg: dict[Sender, Any]) -> None:
        super().receive(msg)

        if isinstance(msg["from"], TicketGrantingServer):
            self.__tgs_ss = msg["message"]
        else:
            send_to_client: tuple = self.process_client_msg(msg)
            self.send(msg["from"], send_to_client)

    def process_client_msg(self, msg: dict[Sender, Any]) -> tuple:
        tgs: tuple = decrypt(msg["message"][:5], self.__tgs_ss)

        client_key, ss, issue_timestamp, ticket_validitity = map(hex2decimal, tgs[:-1])
        c_ss: str = tgs[-1]

        aut_2: tuple[int, ...] = tuple(map(hex2decimal, decrypt(msg["message"][5:], c_ss)))

        if (client_key, issue_timestamp) != aut_2:
            raise ConnectionRefusedError("Invalid TGS / Aut2")

        return encrypt(aut_2[1] + 1, c_ss)
