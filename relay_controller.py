import socket
import json
from config import PLATFORM_RASPBERRY_PI_IS_USED, RELAY_CONTROLLER_IP, RELAY_CONTROLLER_PORT

# Import the appropriate GPIO library based on the platform
if PLATFORM_RASPBERRY_PI_IS_USED:
    import RPi.GPIO as GPIO
else:
    class GPIO:
        BCM = "BCM"
        OUT = "OUT"
        IN = "IN"
        HIGH = True
        LOW = False

        @staticmethod
        def setmode(mode):
            print(f"[MOCK] GPIO set mode: {mode}")

        @staticmethod
        def setup(gpio_num, param):
            print(f"[MOCK] GPIO setup {gpio_num} with param {param}")

        @staticmethod
        def output(gpio_num, state):
            print(f"[MOCK] GPIO {gpio_num} set to {'HIGH' if state else 'LOW'}")

        @staticmethod
        def input(gpio_num):
            state = GPIO.LOW
            print(f"[MOCK] GPIO {gpio_num} read as {'HIGH' if state else 'LOW'}")
            return state

        @staticmethod
        def cleanup():
            print("[MOCK] GPIO cleanup")

# List of GPIOs (initially without state)
gpios = [
    {"num": 1, "state": None},
    {"num": 2, "state": None},
    {"num": 3, "state": None},
    {"num": 4, "state": None},
    {"num": 5, "state": None},
    {"num": 6, "state": None},
    {"num": 7, "state": None},
    {"num": 8, "state": None},
    {"num": 9, "state": None},
    {"num": 10, "state": None}
]

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup all GPIOs as inputs initially
for gpio in gpios:
    GPIO.setup(gpio["num"], GPIO.IN)

def update_gpio_states():
    """Update the gpio list with the current state of each GPIO pin."""
    for gpio in gpios:
        state = GPIO.input(gpio["num"])
        gpio["state"] = "ON" if state == GPIO.HIGH else "OFF"

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
                    # Set the GPIO output based on the state
                    if state == "ON":
                        GPIO.output(gpio_num, GPIO.HIGH)
                    else:
                        GPIO.output(gpio_num, GPIO.LOW)

                    print(f"GPIO {gpio_num} has been turned {state}")
                    response = {"status": "success", "gpio": gpio_num, "state": state}
                    break

        elif action == "get":
            update_gpio_states()  # Refresh GPIO states before sending
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
    server.bind((RELAY_CONTROLLER_IP, RELAY_CONTROLLER_PORT))
    server.listen(5)
    print(f"Relay controller is listening on port {RELAY_CONTROLLER_PORT}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    try:
        start_server()
    finally:
        GPIO.cleanup()  # Clean up GPIO settings on exit
