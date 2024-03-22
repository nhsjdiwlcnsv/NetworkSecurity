from lab3.network.protocols.ip import IP


class TCP:
    """Simulates TCP protocol behavior.

    Is initialized with sender's port, receiver's port, and IP, which contains
    both source IP and destination IP addresses.
    """
    def __init__(self, source_port: int, destination_port: int, ip: IP):
        self.ip = ip
        self.source_port: int = source_port
        self.destination_port: int = destination_port
        self.sequence: int = 0  # tracks byte position within an open stream of data being sent. first is random (ISN)
        self.acknowledgment: int = 0  # should be SEQ + 1
        self.offset: int = 20  # basically represents the length of TCP header
        self.ns = None
        self.cwr = None
        self.ece = None
        self.urg = None
        self.ack: bool = False
        self.psh = None
        self.rst: bool = False
        self.syn: bool = False
        self.fin: bool = False
        self.window_size: int | None = None  # the size of the buffer space available for incoming data
        self.checksum: int = 0  # error-checking checksum
        self.urgent: int | None = None  # points to the end of the urgent data

    def __str__(self) -> str:
        return 'Source socket {}:{} | Destination socket {}:{} | Seq: {} | Ack: {} | Payload: "{}"'.format(
            self.ip.source_ip, self.source_port, self.ip.destination_ip, self.destination_port,
            self.sequence, self.acknowledgment, self.ip.payload)

    def __repr__(self) -> str:
        return str(self)
