import time
from lab3.network.members.member import Member
from lab3.network.middleware.middleware import FakeIpAddressMiddleware, RSTMiddleware
from lab3.network.connection import ConnectionHijack, Connection


def run_attacks():
    client = Member(100, 8000)
    server = Member(200, 5000)

    fakeIpAddressMiddleware = FakeIpAddressMiddleware(1, 1)  # IP-spoofing
    rstMiddleware = RSTMiddleware()  # TCP Reset
    connectionHijack = ConnectionHijack()  # TCP/IP hijacking
    connection = Connection([client, server], [rstMiddleware])

    client.call(connection, 1)


if __name__ == "__main__":
    run_attacks()
