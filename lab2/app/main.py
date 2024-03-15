import os

from dotenv import load_dotenv

from lab2.servers.kerberos import AuthenticationServer, TicketGrantingServer
from lab2.servers.service import ServiceServer
from lab2.client.client import Client
from lab2.utils import generate_user_keys, insert_user_keys


load_dotenv()

DB_PATH: str = os.environ["DB_PATH"]


if __name__ == "__main__":
    # Creating users
    user_keys: list[str] = generate_user_keys(8, 500)

    insert_user_keys(DB_PATH, user_keys)

    # Preparing the servers
    client = Client(user_keys[0])
    auth_server = AuthenticationServer(0, DB_PATH)
    tg_server = TicketGrantingServer(1)
    service_server = ServiceServer(2)

    auth_server.connect_tgs(tg_server)
    tg_server.connect_ss(service_server)

    # Connection attempt
    client.connect(service_server, (auth_server, tg_server))
