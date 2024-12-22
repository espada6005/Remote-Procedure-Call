import socket
import os
import json

class Calculation:
    def floor(self, x):
        return int(x // 1)

    def nroot(self, n, x):
        return x ** (1 / n)

    def reverse(self, s):
        return s[::-1]

    def validAnagram(self, str1, str2):
        return sorted(str1) == sorted(str2)

    def sort(self, strArr):
        return sorted(strArr)

def main():
    calculation_instance = Calculation()

    method_hashmap = {
        "floor": calculation_instance.floor,
        "nroot": calculation_instance.nroot,
        "reverse": calculation_instance.reverse,
        "validAnagram": calculation_instance.validAnagram,
        "sort": calculation_instance.sort,
    }

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    server_address = "./socket_file"

    try:
        os.unlink(server_address)
    except FileNotFoundError:
        pass

    print("Starting up on {}".format(server_address))

    sock.bind(server_address)

    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        try:
            print("connection from", client_address)

            while True:
                data = connection.recv(1024)

                if data:

                    try:
                        data_str = data.decode("utf-8")

                        print("Received data: {}".format(data_str))

                        receivedData = json.loads(data)

                        print(receivedData)

                        method = receivedData["method"]
                        params = receivedData["params"]
                        id = receivedData["id"]

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
                                answer = method_hashmap[method](params)
                            else:
                                answer = method_hashmap[method](*params)

                            print(answer)
                            result_type = str(type(answer)).split("'")[1]
                            print(result_type)

                            response = {
                                "results": answer,
                                "result_type": result_type,
                                "id": id,
                            }

                            print("answer data: {}".format(response))
                        except Exception as e:
                            response = {"error": str(e), "id": id}

                    except json.JSONDecodeError:
                        response = {"error": "Invalid JSON format", "id": None}

                    connection.send(json.dumps(response).encode())
                else:
                    print("no data from", client_address)
                    break

        finally:
            print("Closing current connection")
            connection.close()


main()
