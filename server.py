import socket
import os
import json

class Caliculation:

    @staticmethod
    def floor(x):
        return int(x // 1)
    
    @staticmethod
    def nroot(n, x):
        return x ** (1 / n)
    
    @staticmethod
    def reserve(s):
        return s[::-1]
    
    @staticmethod
    def validAnagram(str1, str2):
        return sorted(str1) == sorted(str2)
    
    @staticmethod
    def sort(strArr):
        return sorted(strArr)

class SocketServer:
    
    @staticmethod
    def setup_server():
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        server_address = "./socket_file"

        try:
            os.unlink(server_address)
        except FileNotFoundError:
            pass

        sock.bind(server_address)