from lab2.servers import Server


class TicketGrantingServer(Server):
    def __init__(self, server_id: int):
        super().__init__(server_id)
