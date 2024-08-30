from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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

# Serve the HTML page at the root URL
@app.route('/')
def index():
    return render_template('index.html', gpios=gpios)

# Handle GPIO POST requests
@app.route('/gpio', methods=['POST'])
def handle_gpio():
    data = request.json
    gpio = int(data.get('gpio'))
    state = data.get('state')

    # Update the state in the gpios list
    for gpio_obj in gpios:
        if gpio_obj["num"] == gpio:
            gpio_obj["state"] = state

    print(f"GPIO {gpio} is {state}")
    return jsonify({'status': 'success', 'gpio': gpio, 'state': state})

if __name__ == '__main__':
    app.run(debug=True)
