# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from base64 import b64encode
import os
import base64 

max_size = 2**24

def no_es_entero(texto):
    try:
        int(texto)
        return False
    except ValueError:
        return True
    
class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """
    
    def __init__(self, socket, directory):
        self.socket = socket
        self.directory = directory

    def get_file_listing(self, args):
        if(len(args)!=1):
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        files = os.listdir(self.directory)
        result = f"{CODE_OK} OK{EOL}"
        for arc in files:
            result += f"{arc}{EOL}"
        result += f"{EOL}"
        return result
    
    def get_metadata(self, args):
        if(len(args)!=2):
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        
        filepath = os.path.join(self.directory, args[1])
        if(not os.path.exists(filepath)): 
                result = f"{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}{EOL}"
                return result
        size = os.path.getsize(filepath) 
        result = f"{CODE_OK} OK{EOL}{size}{EOL}"
        return result

    def get_slice(self, args):

        if(len(args)!=4):
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        if(no_es_entero(args[2]) and no_es_entero(args[3])):
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        
        filepath = os.path.join(self.directory, args[1])
        if(not os.path.exists(filepath)): 
            result = f"{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}{EOL}"
            return result
        with open(filepath, 'rb') as file:
            if(int(args[2]) + int(args[3])>os.path.getsize(filepath)): #si el offset es mayor al tamaño del archivo...
                result = f"{BAD_OFFSET} {error_messages[BAD_OFFSET]}{EOL}"   
                return result
            file.seek(int(args[2]))
            bin_text = file.read(int(args[3])) 
            final_text = base64.b64encode(bin_text).decode("ascii")
            result = f"{CODE_OK} OK{EOL}{final_text}{EOL}"
            return result

    def quit(self, args):
        if(len(args)!=1):
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        return "quit"

    def execute(self, cmd):
        args = cmd.split(' ')
        print(f"EXECUTE   {args}")

        if(args[0]=="get_file_listing"):
            result = self.get_file_listing(args)
        elif (args[0]=="get_metadata"):
            result = self.get_metadata(args)
        elif (args[0]=="get_slice"):
            result = self.get_slice(args)
        elif (args[0]=="quit"):
            result = self.quit(args)
        else: 
            result = f"{INVALID_COMMAND} {error_messages[INVALID_COMMAND]}{EOL}"
        return result
        

    def handle(self):
        buffer = ""
        end = False
        while not end:
                try:
                    # Recibir datos con timeout
                    # self.socket.settimeout(20.0)  # Timeout de 5 segundos
                    data = self.socket.recv(max_size).decode("ascii")
                    
                    if not data: 
                        print("Conexión cerrada por el cliente")
                        end = True
                        break

                    buffer += data
                    print(f"Buffer actual: {repr(buffer)}")  # Debug

                    # Procesar todos los comandos completos
                    while EOL in buffer:
                        # Separar el primer comando completo
                        cmd, buffer = buffer.split(EOL, 1)
                        cmd = cmd.strip()

                        if "\n" in cmd:
                            self.socket.send(f"{BAD_EOL} {error_messages[BAD_EOL]}{EOL}".encode("ascii"))
                            end = True
                            break

                        print(f"Procesando comando: {cmd}")
                        msg = self.execute(cmd)

                        if msg == "quit":
                            self.socket.send(f"{CODE_OK} OK{EOL}".encode("ascii"))
                            end = True
                            break
                        else:
                            self.socket.send(msg.encode("ascii"))

                except socket.error as e:
                    print(f"Error de socket: {e}")
                    self.socket.send(f"{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}{EOL}".encode("ascii"))
                    end = True
    
        self.socket.close()
        print("Conexión cerrada")
