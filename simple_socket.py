import socket
import sys


HOST = '127.0.0.1'
PORT = 65432


def runweb():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Listening on port {PORT}')
        while True:
            conn, addr = s.accept()
            print(f'Connection accepted. {conn} - {addr}')

            data = conn.recv(1024).decode('UTF-8')
            routes = ['/test', '/', '/main']
            route = data.split(' ')[1]

            if route == '/hello':
                conn.send(b'HTTP/1.1 200 OK\n')
                conn.send(b'Content-Type: text/html\n\n')
                conn.send(b'<html><body><h1>Hello World</h1></body></html>')

            elif route == '/test':
                conn.send(b'HTTP/1.1 200 OK\n')
                conn.send(b'Content-Type: text/html\n\n')
                conn.send(b'<html><body><h1 style="color: blue">A different page</h1></body></html>')

            elif route not in routes:
                conn.send(b'HTTP/1.1 400 NOT FOUND\n')
                conn.send(b'Content-Type: text/html\n\n')
                conn.send(b'<html><body><h1 style="color: red">Page not found</h1></body></html>')


def up_host():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Listening on port {PORT}')
        conn, addr = s.accept()
        print('Connection accepted!')
        with conn:
            print('Connected by ', addr)
            while True:
                data = conn.recv(1024)
                data_s = data.decode('UTF-8')
                print(f"Message: {data_s}; received by {addr}")
                if not data: break
                conn.sendall(b"Your message is received")


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello World, socket')
        data = s.recv(1024)
    print('Received', repr(data))


if __name__ == '__main__':
    args = sys.argv
    if args[1] == 'runserver':
        runweb()

    elif args[1] == 'server':
        up_host()

    else:
        client()