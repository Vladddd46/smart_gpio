from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

gpios = [{"num": 1, "state": "OFF"}, 
        {"num": 2, "state": "OFF"}, 
        {"num": 3, "state": "OFF"},
        {"num": 4, "state": "OFF"},
        {"num": 5, "state": "ON"},
        {"num": 6, "state": "OFF"},
        {"num": 7, "state": "OFF"},
        {"num": 8, "state": "OFF"},
        {"num": 9, "state": "OFF"},
        {"num": 10, "state": "OFF"}]

# Serve the HTML page at the root URL
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Handle GPIO POST requests
@app.route('/gpio', methods=['POST'])
def handle_gpio():
    data = request.json
    gpio = data.get('gpio')
    state = data.get('state')
    print(f"GPIO {gpio} is {state}")
    return jsonify({'status': 'success', 'gpio': gpio, 'state': state})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
