#!/usr/bin/python

"""
Simple HTTP Server version 2: reuses the port, so it can be
restarted right after it has been killed. Accepts connects from
the outside world, by binding to the primary interface of the host.
Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind((socket.gethostname(), 1235))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

try:
    almacenado = False
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('Request received:')
        peticion = recvSocket.recv(2048).decode("utf-8", "strict")
        print(peticion)
        recurso = peticion.split()[1][1:]
        if recurso == "favicon.ico":
            recvSocket.send(bytes(
                            "HTTP/1.1 404 Not Found\r\n\r\n" +
                            "<html><body><h1>Not Found</h1></body></html>" +
                            "\r\n", "utf-8"))
            recvSocket.close()
            continue
        try:
            if almacenado is False:
                sumando = int(recurso)
                almacenado = True
                recvSocket.send(bytes(
                                "HTTP/1.1 200 OK\r\n\r\n" +
                                "<html><body><h1>Almacenado el numero: </h1>" +
                                str(sumando) +
                                "</body></html>" +
                                "\r\n", "utf-8"))
                recvSocket.close()
            else:
                suma = sumando+int(recurso)
                almacenado = False
                recvSocket.send(bytes(
                                "HTTP/1.1 200 OK\r\n\r\n" +
                                "<html><body><h1>El resultado de la" +
                                " suma es: </h1>" +
                                str(sumando) + "+" + recurso + "=" +
                                str(suma) +
                                "</body></html>" +
                                "\r\n", "utf-8"))
                recvSocket.close()
        except ValueError:
            almacenado = False
            recvSocket.send(bytes(
                            "HTTP/1.1 404 NOT FOUND\r\n\r\n" +
                            "<html><body><h1>Introduce un numero</h1>" +
                            "</body></html>" +
                            "\r\n", "utf-8"))
            recvSocket.close()
except KeyboardInterrupt:
    print("Closing binded socket")
mySocket.close()
