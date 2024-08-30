import socket
import json

# List of GPIO states
gpios = [
    {"num": 1, "state": "OFF"},
    {"num": 2, "state": "OFF"},
    {"num": 3, "state": "OFF"},
    {"num": 4, "state": "OFF"},
    {"num": 5, "state": "ON"},
    {"num": 6, "state": "OFF"},
    {"num": 7, "state": "OFF"},
    {"num": 8, "state": "OFF"},
    {"num": 9, "state": "OFF"},
    {"num": 10, "state": "OFF"}
]

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    
    try:
        data = json.loads(request)
        action = data.get("action")

        if action == "update":
            gpio_num = data.get("gpio")
            state = data.get("state")

            for gpio in gpios:
                if gpio["num"] == gpio_num:
                    gpio["state"] = state
                    print(f"GPIO {gpio_num} has been turned {state}")
                    response = {"status": "success", "gpio": gpio_num, "state": state}
                    break

        elif action == "get":
            response = {"status": "success", "gpios": gpios}

        else:
            response = {"status": "error", "message": "Invalid action"}
            print("Received an invalid action request")

    except json.JSONDecodeError:
        response = {"status": "error", "message": "Invalid JSON format"}
        print("Received an invalid JSON request")

    client_socket.send(json.dumps(response).encode())
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 65432))
    server.listen(5)
    print("Relay controller is listening on port 65432...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
