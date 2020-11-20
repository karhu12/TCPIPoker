import asyncio
from tcp_ip_poker.poker import TexasHoldem, Player


connections = {}
games = []

class PokerGameServerProtocol(asyncio.Protocol):
    MAX_DATA_LEN = 1024
    ENCODE_PROTOCOL = 'utf-8'

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print("New connection from {}".format(peername))
        self.transport.write('Welcome to the poker game server!\nSend your username to join a lobby > '.encode(self.ENCODE_PROTOCOL))

    def data_received(self, data):
        message = data.decode()
        addr = self.transport.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")
        print(f"Send: {message!r}")
        self.transport.write(data)
        self.transport.close()

async def main():
    server = await asyncio.start_server(PokerGameServerProtocol(), '0.0.0.0', 8888)

    print(f'Serving server on {server.sockets[0].getsockname()}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())


