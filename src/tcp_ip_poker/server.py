import asyncio

async def server_handler(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(server_handler, '0.0.0.0', 8888)

    print(f'Serving server on {server.sockets[0].getsockname()}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())


