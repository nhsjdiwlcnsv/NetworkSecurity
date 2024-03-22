from lab3.network.connection import Connection
from lab3.network.protocols.ip import IP
from lab3.network.protocols.tcp import TCP


class Member:
    def __init__(self, ip_address: int, tcp_port: int):
        self.ip_address: int = ip_address
        self.tcp_port: int = tcp_port
        self.caller: bool = False

    def call(self, connection: Connection, index: int):
        self.caller = True
        other = connection.endponts[index]
        package = self._build_package(other, self._generate_payload())
        connection.send(package)

    def _build_package(self, receiver, payload):
        ip = IP(self.ip_address, receiver.ip_address, payload)
        tcp = TCP(self.tcp_port, receiver.tcp_port, ip)

        tcp.sequence = 0
        tcp.syn = True

        return tcp

    def _build_answer(self, package, payload: str):
        ip = IP(package.ip.destination_ip, package.ip.source_ip, payload)
        response = TCP(package.destination_port, package.source_port, ip)

        # Receival acknowledgement
        if package.syn and package.ack:
            response.sequence = package.acknowledgment
            response.acknowledgment = package.sequence + 1
            response.ack = True
            return response

        # Initial synchronization request
        if package.syn and not package.ack:
            response.sequence = 0
            response.acknowledgment = package.sequence + 1
            response.syn = True
            response.ack = True
            return response

        # Complete three-way handshake
        if package.ack:
            response.sequence = package.acknowledgment
            response.acknowledgment += len(payload) // 8
            response.ip.payload = "Connection acknowledged"
            return response

        response.ip.payload = payload

        if self.caller:
            response.sequence = package.acknowledgment
            response.acknowledgment = package.sequence + len(payload) // 8
        else:
            response.sequence = package.acknowledgment
            response.acknowledgment = package.sequence

        return response

    def _generate_payload(self):
        return "Payload from member with address {}:{}".format(self.ip_address, self.tcp_port)

    def receive(self, package):
        answer = self._build_answer(package, self._generate_payload())
        return answer
