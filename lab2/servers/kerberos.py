import os
from time import time
from sys import stderr
from typing import Any

from lab2 import Sender
from lab2.servers import Server
from lab2.utils.crypto import encrypt, decrypt, des_round
from lab2.utils.helpers import hex2decimal


class AuthenticationServer(Server):
    def __init__(self, server_id: int, db_path: str):
        super().__init__(server_id)

        assert os.path.exists(db_path)

        self.db_path: str = db_path
        self.ticket_validity: int = 60
        self._tgs: Server | None = None
        self.__as_tgs: str | None = None
        self.__c_tgs: str | None = None

    def _verify_user_key(self, key: str) -> None:
        with open(self.db_path, "r") as db:
            if key not in db.read().split("\n"):
                raise ConnectionRefusedError(f"Couldn't find user with key {key} in the database!")

    def receive(self, msg: dict[Sender, Any]) -> None:
        super().receive(msg)
        self.send_tgs_key(msg["message"])

    def connect_tgs(self, tgs) -> None:
        self._tgs = tgs

    def _generate_c_tgs(self) -> str:
        try:
            self.__c_tgs = self._tgs.keygen()
            return self.__c_tgs
        except AttributeError:
            print("Ticket Granting Server is not connected!", file=stderr)
            return ""

    def _get_tgt(self, client_key: int) -> tuple[int, int, int, int, str] | None:
        self._generate_c_tgs()

        try:
            return client_key, self._tgs.server_id, int(time()), self.ticket_validity, self.__c_tgs
        except AttributeError:
            print("Ticket Granting Server is not connected!", file=stderr)

    def send_tgs_key(self, client) -> None:
        self._verify_user_key(client.key)

        tgt: tuple[int, int, int, int, str] = self._get_tgt(client.intkey)
        self.__as_tgs = self.keygen()
        enc_tgt: tuple = encrypt(tgt, key=self.__as_tgs)
        msg: tuple = encrypt([*enc_tgt, self.__c_tgs], key=client.key)

        self.send(recipient=self._tgs, msg=self.__as_tgs)
        self.send(recipient=client, msg=msg)


class TicketGrantingServer(Server):
    def __init__(self, server_id: int):
        super().__init__(server_id)
        self.ticket_validity: int = 60

    def receive(self, msg: dict[Sender, Any]) -> None:
        super().receive(msg)

        if isinstance(msg["from"], AuthenticationServer):
            self.__as_tgs = msg["message"]
        else:
            # self.send_ss_key()
            send_to_client: tuple = self.process_client_msg(msg)
            self.send(msg["from"], send_to_client)

    def process_client_msg(self, msg: dict[Sender, Any]) -> tuple:
        tgt: tuple[str, ...] = decrypt(msg["message"][:5], self.__as_tgs)
        client_key, tgs, issue_timestamp, ticket_validity = map(hex2decimal, tgt[:-1])
        c_tgs: str = tgt[-1]

        aut_1: tuple[int, int] = tuple(map(hex2decimal, decrypt(msg["message"][5:7], c_tgs)))
        sid: int = msg["message"][-1]

        if (client_key, issue_timestamp) != aut_1:
            raise ConnectionRefusedError("Invalid TGT / Aut1")

        self._generate_c_ss()

        ticket_gs: tuple = client_key, sid, int(time()), self.ticket_validity, self.__c_ss
        self.__tgs_ss: str = self.keygen()

        self.send(self._ss, self.__tgs_ss)

        return encrypt([*encrypt(ticket_gs, self.__tgs_ss), self.__c_ss], c_tgs)

    def connect_ss(self, ss) -> None:
        self._ss = ss

    def _generate_c_ss(self) -> str:
        try:
            self.__c_ss = self._ss.keygen()
            return self.__c_ss
        except AttributeError:
            print("Ticket Granting Server is not connected!", file=stderr)
            return ""
