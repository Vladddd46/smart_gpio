<h1>Smart gpio</h1>
<p>Project for remote control of gpios on Raspberry Pi</p>

<h3>Quick start</h3>
<p>1. Need python3 installed</p>
<p>2. run from terminal: pip install -r requirements.txt</p>
<p>3. start raspberry pi controller server: python relay_controller.py</p>
<p>4. start flask web interface: python main.py</p>
<p>Go to http://127.0.0.1:5000/ from browser</p>
<p>Note: if you run the project on raspberry pi, then you also need to install gpio module(on other platforms mock is used): pip3 install RPi.GPIO</p>