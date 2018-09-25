from request import Request
from router import Router

import controller 
import socket

# create a server listening on port 8888
HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...' % PORT)

while True:
  
    client_connection, client_address = listen_socket.accept()
    # we listen for a request. Then we need to convert it from bytes to a string with decode. 
    request_text = client_connection.recv(1024).decode('utf-8')
    request = Request(request_text)
 
    response = Router.process(request)
   
    client_connection.send( str(response).encode() )

    client_connection.close()

   
    
