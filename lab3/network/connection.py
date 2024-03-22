import time
from datetime import datetime
from typing import Any

from lab3.network.protocols.tcp import TCP


def print_package(package):
    try:
        time.sleep(1.5)

        msg: str = f"| Next package. {package} |"
        frame_len: int = len(msg)

        print(f"{datetime.now()}\n{'-' * frame_len}\n{msg}\n{'-' * frame_len}\n\n")
    except KeyboardInterrupt:
        raise BaseException("Interrupted by user")


class Connection:
    def __init__(self, endpoints: list[Any] | tuple[Any], middlewares: list[Any] | tuple[Any]):
        self.endponts: list[Any] | tuple[Any] = endpoints
        self.middlewares: list[Any] | tuple[Any] = middlewares
        self.closed: bool = False
        self.connected: bool = False

    def _find_receiver(self, package: TCP):
        for endpoint in self.endponts:
            if (endpoint.ip_address == package.ip.destination_ip and endpoint.tcp_port == package.destination_port):
                return endpoint

    def send(self, package: TCP):
        self.connected = True
        self.process(package)

    def process(self, package: TCP):
        if not self.connected or self.closed:
            return

        print_package(package)

        for middleware in self.middlewares:
            package = middleware.change(package)

        if package.rst:
            print("Package RST flag set")
            self.close()
            return

        package.ip.ttl -= 1
        if package.ip.ttl <= 0:
            print('Package TTL is expired')
            self.close()
            return

        receiver = self._find_receiver(package)

        if receiver is None:
            print('Unknown destination {}:{}'.format(package.ip.destination_ip, package.destination_port))
            self.close()
            return

        package = receiver.receive(package)
        if package is None:
            print('One of members stop sending requests')
            self.close()
        else:
            self.process(package)

    def close(self):
        self.closed = True
        print('Connection is closed')


class ConnectionHijack:
    def __init__(self):
        self.call_number = 0

    def change(self, package):
        self.call_number += 1
        if self.call_number >= 5:
            package.ip.payload = "Connection hijacked"
            t = package.sequence
            package.sequence = package.acknowledgment
            package.acknowledgment = t + len(package.ip.payload)
            package.ip.destination_ip = package.ip.source_ip
            package.destination_port = package.source_port
            print_package(package)
        return package
