# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from typing import List, Tuple, Optional
from constants import *
from base64 import b64encode
import os
import base64 

max_size: int = 2**24

def no_es_entero(texto: str) -> bool:
    """Verifica si un texto no puede convertirse a entero.
    
    Args:
        texto: Texto a verificar.
        
    Returns:
        True si no es convertible a entero, False si lo es.
    """
    try:    #Intento castear el texto a un valor numerico entero
        int(texto)
        return False
    except ValueError:  #de no poderse, es porque no es entero
        return True


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.

    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """
    
    def __init__(self, socket: socket.socket, directory: str) -> None:
        """Inicializa una nueva conexión con un cliente.
        
        Args:
            socket: Socket de conexión con el cliente.
            directory: Directorio compartido por el servidor.
        """
        self.socket = socket
        self.directory = directory

    def get_file_listing(self, args: List[str]) -> str:
        """
        Maneja el comando que obtiene el listado de archivos en el directorio
        compartido.
        
        Args:
            args: Lista de argumentos del comando (debe contener solo 1
            elemento).
            
        Returns:
            Respuesta formateada con el listado de archivos o mensaje de error.
        """
        if len(args) != 1:  #manejo de error "Cantidad de argumentos"
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        files = os.listdir(self.directory)  #files = <directory>/
        result = f"{CODE_OK} OK{EOL}"
        for arc in files:   #arc -> {foo, bar, x}
            result += f"{arc}{EOL}"
        result += f"{EOL}"
        return result
    
    def get_metadata(self, args: List[str]) -> str:
        """
        Maneja el comando que obtiene los metadatos (tamaño) de un archivo
        específico.
        
        Args:
            args: Lista de argumentos (debe contener 2 elementos: comando
                y nombre de archivo).
            
        Returns:
            Respuesta con el tamaño del archivo o mensaje de error.
        """
        if len(args) != 2:  #manejo de error "Cantidad de argumentos"
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        filepath = os.path.join(self.directory, args[1])
        if not os.path.exists(filepath):    #manejo de error "Archivo no existe"
            result = f"{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}{EOL}"
            return result
        size = os.path.getsize(filepath)    #size = <tamaño de "filepath">
        result = f"{CODE_OK} OK{EOL}{size}{EOL}"
        return result

    def get_slice(self, args: List[str]) -> str:
        """
        Maneja el comando que obtiene un fragmento de un archivo en formato
        base64.
        
        Args:
            args: Lista de argumentos (debe contener 4 elementos: comando,
                nombre de archivo, offset y tamaño del fragmento).
                        
        Returns:
            Respuesta con el fragmento en base64 o mensaje de error.
        """
        if len(args) != 4:  #manejo de error "Cantidad de argumentos"
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        if no_es_entero(args[2]) or no_es_entero(args[3]):  
            #manejo de error "Argumentos en valores enteros"
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        filepath = os.path.join(self.directory, args[1])
        if not os.path.exists(filepath):    #manejo de error "Archivo no existe"
            result = f"{FILE_NOT_FOUND} {error_messages[FILE_NOT_FOUND]}{EOL}"
            return result
        with open(filepath, 'rb') as file:  #file = "filepath" en lectura
            if int(args[2]) + int(args[3]) > os.path.getsize(filepath):
                    #manejo de error "In bounds"
                result = f"{BAD_OFFSET} {error_messages[BAD_OFFSET]}{EOL}"   
                return result
            file.seek(int(args[2])) #empieza a leer desde "args[2]"
            bin_text = file.read(int(args[3]))  #lee "args[3]" de bits
            final_text = base64.b64encode(bin_text).decode("ascii")
                #final_text = <texto leido en base64>
            result = f"{CODE_OK} OK{EOL}{final_text}{EOL}"
            return result

    def quit(self, args: List[str]) -> str:
        """Maneja el comando para finalizar la conexión.
        
        Args:
            args: Lista de argumentos (debe contener solo 1 elemento).
            
        Returns:
            "quit" si el comando es válido, mensaje de error en caso contrario.
        """
        if len(args) != 1:  #manejo de error "Cantidad de argumentos"
            result = f"{INVALID_ARGUMENTS} {error_messages[INVALID_ARGUMENTS]}{EOL}"
            return result
        return "quit"

    def execute(self, cmd: str) -> str:
        """Ejecuta el comando recibido del cliente.
        
        Args:
            cmd: Comando recibido del cliente.
            
        Returns:
            Respuesta correspondiente al comando ejecutado.
        """
        args = cmd.split(' ')
        #veo con que clase de comando estoy tratando
        if args[0] == "get_file_listing": 
            result = self.get_file_listing(args)
        elif args[0] == "get_metadata":
            result = self.get_metadata(args)
        elif args[0] == "get_slice":
            result = self.get_slice(args)
        elif args[0] == "quit":
            result = self.quit(args)
        else:   #manejo de error "Comando invalido"
            result = f"{INVALID_COMMAND} {error_messages[INVALID_COMMAND]}{EOL}"
        return result
        

    def handle(self) -> None:
        """
        Maneja la conexión con el cliente, procesando los comandos recibidos.
        """
        buffer = ""
        end = False
        while not end: #hasta que el usuario termine la conexion
            try: #intento hacer uso del socket
                #recibo lo  que envió el usuario por el socket
                data = self.socket.recv(max_size).decode("ascii")
                #si no mandó nada, termino
                if not data: 
                    print("Conexión cerrada por el cliente")
                    end = True
                    break
                buffer += data
                while EOL in buffer: #mientras haya al menos un comando completo
                    cmd, buffer = buffer.split(EOL, 1)
                    cmd = cmd.strip() #eliminamos espacios en blanco
                    if "\n" in cmd: #manejo de error "Comando malformado"
                        self.socket.send(f"{BAD_EOL} {error_messages[BAD_EOL]}{EOL}".encode("ascii"))
                        end = True
                        break
                    msg = self.execute(cmd)
                    if msg == "quit": #el cliente termina la conexion
                        self.socket.send(f"{CODE_OK} OK{EOL}".encode("ascii"))
                        end = True
                        break
                    else:
                        #enviamos la respuesta por el socket
                        self.socket.send(msg.encode("ascii")) 
            except socket.error as e: #error de socket
                print(f"Error de socket: {e}")
                self.socket.send(f"{INTERNAL_ERROR} {error_messages[INTERNAL_ERROR]}{EOL}".encode("ascii"))
                end = True
        self.socket.close() #cierro el socket
        print("Conexión cerrada")