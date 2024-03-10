import os
import datetime
from sys import stderr
from time import time
from typing import Any
from lab2.servers import Server
from lab2.servers.tgserver import TicketGrantingServer
from lab2.client.client import Client
from lab2.utils.crypto import encrypt


class AuthenticationServer(Server):
    def __init__(self, server_id: int, db_path: str):
        super().__init__(server_id)

        assert os.path.exists(db_path)

        self.db_path: str = db_path
        self.ticket_validity: int = 60
        self._tgs: TicketGrantingServer | None = None

    def _verify_user_key(self, key: str) -> None:
        with open(self.db_path, "r") as db:
            if key not in db.read().split("\n"):
                raise ConnectionRefusedError(f"Couldn't find user with key {key} in the database!")

    def receive(self, msg: Any) -> None:
        self.send_tgs_key(msg)

    def connect_tgs(self, tgs: TicketGrantingServer) -> None:
        self._tgs = tgs

    def _get_c_tgs(self) -> str | None:
        try:
            return self._tgs.keygen()
        except AttributeError:
            print("Ticket Granting Server is not connected!", file=stderr)

    def _get_tgt(self, client_key: int) -> tuple[int, int, int, int, str] | None:
        try:
            return client_key, self._tgs.server_id, int(time()), self.ticket_validity, self._get_c_tgs()
        except AttributeError:
            print("Ticket Granting Server is not connected!", file=stderr)

    def send_tgs_key(self, client: Client) -> None:
        self._verify_user_key(client.key)

        tgt: tuple[int, int, int, int, str] = self._get_tgt(client.intkey)
        as_tgs: str = self.keygen()
        enc_tgt: tuple = encrypt(tgt, key=as_tgs)

        msg: tuple = encrypt([*enc_tgt, self._get_c_tgs()], key=client.key)

        self.send(recipient=client, msg=msg)
