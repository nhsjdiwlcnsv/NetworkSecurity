from typing import Any, Iterable
from time import time

import colorama

from lab2 import Listener, Sender
from lab2.servers import Server
from lab2.servers.kerberos import AuthenticationServer, TicketGrantingServer
from lab2.servers.service import ServiceServer
from lab2.utils.crypto import decrypt, encrypt
from lab2.utils.helpers import hex2decimal


colorama.init(autoreset=True)


class Client(Listener, Sender):
    def __init__(self, key: str):
        self.__key = key
        self.__server: ServiceServer | None = None
        self.__c_tgs: str | None = None

        self.__send_to_tgs: tuple[str, ...] | None = None
        self.__send_to_ss: tuple[str, ...] | None = None

    def receive(self, msg: dict[Sender, Any]) -> None:
        super().receive(msg)

        if isinstance(msg["from"], AuthenticationServer):
            self.__send_to_tgs = self._process_auth_server_msg(msg)
        elif isinstance(msg["from"], TicketGrantingServer):
            self.__send_to_ss = self._process_ticket_granting_server_msg(msg)
        elif isinstance(msg["from"], ServiceServer):
            self.ss_validity: bool = (self._process_service_server_msg(msg) - 1 == self.__aut_2[1])

    def connect(self, server: ServiceServer, aux_servers: tuple[AuthenticationServer, TicketGrantingServer]) -> bool:
        self.__server = server
        auth_server: AuthenticationServer = aux_servers[0]
        tg_server: TicketGrantingServer = aux_servers[1]

        self.send(auth_server, self)  # Steps 1 and 2
        self.send(tg_server, self.__send_to_tgs)  # Steps 3 and 4
        self.send(self.__server, self.__send_to_ss)  # Steps 5 and 6

        if self.ss_validity:
            print(f"Connection status: {colorama.Fore.GREEN + 'success'}")
        else:
            print(f"Connection status: {colorama.Fore.RED + 'failure'}")

    def _process_auth_server_msg(self, msg: dict[Sender, Any]) -> tuple:
        data: tuple[str, ...] = decrypt(msg["message"], self.key)

        tgt, self.__c_tgs = data[:-1], data[-1]
        aut_1: tuple[int, int] = self.intkey, int(time())

        return *tgt, *encrypt(aut_1, self.__c_tgs), self.__server.server_id

    def _process_ticket_granting_server_msg(self, msg: dict[Sender, Any]) -> tuple:
        data: tuple[str, ...] = decrypt(msg["message"], self.__c_tgs)

        tgs, self.__c_ss = data[:-1], data[-1]
        self.__aut_2: tuple[int, int] = self.intkey, int(time())

        return *tgs, *encrypt(self.__aut_2, self.__c_ss)

    def _process_service_server_msg(self, msg: dict[Sender, Any]) -> int:
        return hex2decimal(decrypt(msg["message"], self.__c_ss))

    @property
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, new_key: str) -> None:
        raise AttributeError("Cannot assign new key to the user!")

    @property
    def intkey(self) -> int:
        return sum(map(lambda x: ord(x), self.key))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} #{self.key}"

    def __str__(self) -> str:
        return self.__repr__()
