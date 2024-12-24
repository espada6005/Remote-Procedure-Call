import socket
import os
import json

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
            id = received_data["id"]
            method = received_data["method"]
            params = received_data["params"]


            if method == "floor":
                params = [float(param) for param in params]
            elif method == "nroot":
                params = [int(param) for param in params]
            else:
                params = [str(param) for param in params]

            answer = None
            if method == "sort":
                answer = self.method_hashmap[method](params)
            else:
                answer = self.method_hashmap[method](*params)

            result_type = str(type(answer)).split("'")[1]

            response = {
                "id": id,
                "result_type": result_type,
                "results": answer,
            }
        except Exception as e:
            response = {"error": str(e), "id": received_data.get("id")}
        except json.JSONDecodeError:
            response = {"id": None, "error": "Invalid JSON format"}

        return json.dumps(response).encode()

class SocketServer:
    def __init__(self, server_address, handler):
        self.server_address = server_address
        self.handler = handler
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def start_server(self):
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass

        print(f"開始: {self.server_address}")
        self.sock.bind(self.server_address)
        self.sock.listen(1)

        while True:
            connection, client_address = self.sock.accept()
            try:
                while True:
                    data = connection.recv(1024)
                    if data:
                        print(f"受信データ: {data.decode("utf-8")}")
                        response = self.handler.handle_request(data)
                        print(f"返却データ: {response.decode("utf-8")}")
                        connection.send(response)
                    else:
                        break
            finally:
                print("接続が閉じられました")
                connection.close()

if __name__ == "__main__":
    request_handler = RequestHandler()
    server_address = "./socket_file"
    socket_server = SocketServer(server_address, request_handler)
    socket_server.start_server()
