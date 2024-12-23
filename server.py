import socket
import os
import json

POST = 8080
ADDRESS = "localhost"

class Calculation:
    @staticmethod
    def floor(x):
        return int(x // 1)

    @staticmethod
    def nroot(n, x):
        return x ** (1 / n)

    @staticmethod
    def reverse(s):
        return s[::-1]

    @staticmethod
    def validAnagram(str1, str2):
        return sorted(str1) == sorted(str2)

    @staticmethod
    def sort(strArr):
        return sorted(strArr)

class RequestHandler:
    def __init__(self):
        self.method_hashmap = {
            "floor": Calculation.floor,
            "nroot": Calculation.nroot,
            "reverse": Calculation.reverse,
            "validAnagram": Calculation.validAnagram,
            "sort": Calculation.sort,
        }

    def handle_request(self, data):
        try:
            received_data = json.loads(data)
            method = received_data["method"]
            params = received_data["params"]
            id = received_data["id"]

            if method == "floor":
                params = [float(param) for param in params]
            elif method == "nroot":
                params = [int(param) for param in params]
            else:
                params = [str(param) for param in params]

            print(params)

            try:
                answer = None
                if method == "sort":
                    answer = self.method_hashmap[method](params)
                else:
                    answer = self.method_hashmap[method](*params)

                print(answer)
                result_type = str(type(answer)).split("'")[1]

                response = {
                    "id": id,
                    "result_type": result_type,
                    "results": answer,
                }

                print("answer data: {}".format(response))
            except Exception as e:
                response = {"id": id, "error": str(e)}

        except json.JSONDecodeError:
            response = {"id": None, "error": "Invalid JSON format"}

        return json.dumps(response).encode()

class UDPServer:
    def __init__(self, address, port, handler):
        self.server_address = (address, port)
        self.handler = handler
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_server(self):
        print("Starting up on {}".format(self.server_address))
        self.sock.bind(self.server_address)

        while True:
            data, address = self.sock.recvfrom(4096)
            if data:
                print("Received data: {}".format(data.decode("utf-8")))
                response = self.handler.handle_request(data)
                self.sock.sendto(response, address)

if __name__ == "__main__":
    request_handler = RequestHandler()
    server = UDPServer(ADDRESS, POST, request_handler)
    server.start_server()
