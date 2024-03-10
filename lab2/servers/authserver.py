import os
import datetime
from time import time
from lab2.servers import Server


class AuthenticationServer(Server):
    def __init__(self, server_id: int, db_path: str):
        super().__init__(server_id)

        assert os.path.exists(db_path)

        self.db_path: str = db_path
        self.ticket_validity: int = 60

    def _verify_user_key(self, key: str) -> None:
        with open(self.db_path, "r") as db:
            if key not in db.read().split("\n"):
                raise ConnectionRefusedError(f"Couldn't find user with key {key} in the database!")

    def get_c_tgs(self) -> str:
        return os.urandom(8).hex().upper()

    def get_tgt(self, user_key: str) -> tuple[str, int, int, str]:
        self._verify_user_key(user_key)
        return user_key, self._server_id, int(time()), self.get_c_tgs()
