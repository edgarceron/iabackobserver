import asyncio

port = 20333
host = '127.0.0.1'

loop = asyncio.get_event_loop()

async def open_con(loop): 
    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    message = f'webserver,aaa,3\n'
    writer.write(str.encode(message))
    message = f'label1,total,10\n'
    writer.write(str.encode(message))
    message = f'label1,success,1\n'
    writer.write(str.encode(message))

    a = await reader.read()
    print(a)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(open_con(loop))
    finally:
        # Shutdown the loop even if there is an exception
        loop.close()