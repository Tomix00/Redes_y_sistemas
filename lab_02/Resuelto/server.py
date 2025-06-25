#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
from typing import Tuple, Optional
import connection
from constants import *
import sys
import threading
import os 

class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr: str = DEFAULT_ADDR, port: int = DEFAULT_PORT,
                 directory: str = DEFAULT_DIR) -> None:
        """
        Inicializa el servidor con la configuración especificada.
        
        Args:
            addr: Dirección IP donde escuchar (por defecto DEFAULT_ADDR).

            port: Puerto TCP donde escuchar (por defecto DEFAULT_PORT).

            directory: Directorio compartido (por defecto DEFAULT_DIR).
        """
        print("Serving %s on %s:%s." % (directory, addr, port))
        #creamos el socket
        self.base_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not os.path.isdir(directory):    #creamos el directorio
            os.mkdir(directory)  
        self.directory: str = directory
        base_address = (addr, port)
        self.base_socket.bind(base_address) #conecta el socket

    def serve(self) -> None:
        """
        Loop principal del servidor. Acepta conexiones y las maneja en hilos
        separados.
        """
        self.base_socket.listen(2)

        while True:
            actual_socket, actual_address = self.base_socket.accept()
            print(f"Connected by: {actual_address}")
            client_thread = threading.Thread(   #1 hilo por c/cliente
                target=self.handle_client,
                args=(actual_socket,)
            )
            client_thread.daemon = True  
            client_thread.start()

    def handle_client(self, client_socket: socket.socket) -> None:
        """Maneja una conexión con un cliente.
        
        Args:
            client_socket: Socket de conexión con el cliente.
        """
        actual_connection = connection.Connection(client_socket, self.directory)
        actual_connection.handle()  #aislamos el hadle por cliente


def main() -> None:
    """
    Función principal que parsea los argumentos y lanza el servidor.
    """
    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)
    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)
    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()