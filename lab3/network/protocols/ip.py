class IP:
    """Simulates IP protocol behavior.

    Is initialized with sender's IP, receiver's IP, and data to send
    """
    def __init__(self, source_ip: int, destination_ip: int, payload: str):
        self.version: int = 4
        self.ihl: int = 5  # internet header length
        self.dscp: int | None = None  # differentiated services code point
        self.ecn: int | None = None  # explicit congestion notification
        self.total_length: int = 576
        self.id: int | None = None
        self.flags: int | None = None
        self.fragment_offset: int | None = None
        self.ttl: int = 15  # time to live
        self.protocol: int = 6  # TCP code, UDP is 17
        self.checksum: int | None = None
        self.source_ip: int = source_ip  # sender's IP
        self.destination_ip: int = destination_ip  # receiver's IP
        self.payload: str = payload  # the data of the package
