import asyncio, enum
from tcp_ip_poker.poker import TexasHoldem, Player
from typing import Union


class ConnectionState(enum.Enum):
    AWAITNG_USERNAME = enum.auto()
    USERNAME_CONFIRMATION = enum.auto()
    NOT_READY = enum.auto()
    READY = enum.auto()
    AWAITING_TURN = enum.auto()
    AWAITING_MOVE = enum.auto()

class Commands(enum.Enum):
    CHECK = 'check'
    FOLD = 'fold'
    CLOSE = 'close'

class ServerGameController:
    def __init__(self):
        self._connections = {}
        self._games = []

    CONNECTION_CLOSED = 'connection closed'

    def handle_connection(self, host: str, data: Union[str, None]) -> str:
        if host not in self._connections:
            print("New connection from {}".format(host))
            self._connections[host] = {
                'state': ConnectionState.AWAITNG_USERNAME,
                'player': None
            }
            return '♤ Welcome to the Texas Hold\'em server ♤\r\nEnter your username'
        else:
            return self._handle_state(host, data)

    def _handle_state(self, host: str, data: str) -> str:
        print("Received '{}' from {}".format(data, host))
        try:
            cmd = Commands(data)
            if cmd == Commands.CLOSE:
                return self.CONNECTION_CLOSED
            return 'unhandled command'
        except ValueError:
            return 'unknown command'
        except Exception as e:
            return 'error occured: {}'.format(e)

controller = ServerGameController()

class ServerProtocol(asyncio.Protocol):
    MAX_DATA_LEN = 1024
    ENCODER = 'utf-8'

    def __init__(self, controller: ServerGameController):
        super().__init__()
        self.controller = controller

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        response = self.controller.handle_connection(peername, None)
        self.transport.write((response + '\r\n').encode(self.ENCODER))

    def data_received(self, data):
        message = data.decode(self.ENCODER).replace('\r\n', '')
        peername = self.transport.get_extra_info('peername')
        response = self.controller.handle_connection(peername, message)
        self.transport.write((response + '\r\n').encode(self.ENCODER))
        if response == ServerGameController.CONNECTION_CLOSED:
            print("Connection closed to {}".format(peername))
            self.transport.close()

async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: ServerProtocol(controller), '0.0.0.0', 8888)

    print(f'Serving server on {server.sockets[0].getsockname()}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())


