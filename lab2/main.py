import os
from dotenv import load_dotenv
from lab2.servers.authserver import AuthenticationServer
from lab2.servers.tgserver import TicketGrantingServer
from lab2.servers.serviceserver import ServiceServer
# from lab2.servers.kdcserver import KerberosServer
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

    # Steps 1 and 2
    client.send(auth_server, client)

    # Step 3
    client.send(tg_server, "")

    # Step 4
    tg_server.send(client, "")

    # Step 5
    client.send(service_server, "")

    # Step 6
    service_server.send(client, "")
