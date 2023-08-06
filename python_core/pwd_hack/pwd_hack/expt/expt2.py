import socket

client_socket = socket.socket()
host = '127.0.0.1'
port = 8000
address = (host, port)
# client_socket.connect(address)
data = "Panda, hello"
client_socket.send(data.encode())
