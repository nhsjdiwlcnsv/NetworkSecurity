import os
from dotenv import load_dotenv
from lab2.servers.authserver import AuthenticationServer
# from lab2.servers.kdcserver import KerberosServer
# from lab2.servers.tgserver import TicketGranringServer
# from lab2.servers.serviceserver import ServiceServer
from lab2.client.client import Client


load_dotenv()


if __name__ == "__main__":
    client = Client("AyCtyTMSEY2a")
    auth_server = AuthenticationServer(0, os.environ["DB_PATH"])

    client.send(auth_server, client.key)
