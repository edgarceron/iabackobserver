import socket
from _thread import start_new_thread

host = '127.0.0.1'
port = 1233
ThreadCount = 0

LABEL_SERVER = 'webserver'

def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)

def client_handler(connection: socket.socket, data: dict):
    connection.send(str.encode('You are now connected to the replay server...'))
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        label, key, value = tuple(message.split(','))

        if label == LABEL_SERVER: 
            data['webserver'] = connection
            data['labels'] = value
            continue

        if key == 'BYE': break
        elif key == 'conn': data[label] = {}
        elif key == 'total': data[label]['total'] = value
        elif key == 'success': data[label]['success'] = data[label].get('success', 0) + 1
        elif key == 'fail': data[label]['fail'] = data[label].get('fail', 0) + 1

        count = 0
        total = 0
        for i in data.keys():
            if i == 'webserver' or i == 'labels': continue
            total += data[i]['total']
            count += data[i]['success']
            count += data[i]['fail']

        advance_percentage = str(int(count/total * 100))
        reply = f'advance,{advance_percentage}'
        data['webserver'].sendall(str.encode(reply))
    connection.close()

def accept_connections(ServerSocket: socket.socket):
    Client, address = ServerSocket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')
    start_new_thread(client_handler, (Client, )) 

start_server(host, port)