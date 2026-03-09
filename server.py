from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import threading
import time
import webbrowser
import socket
import serial

try:
    arduino = serial.Serial('COM5', 9600, timeout=1)  
    time.sleep(2)
    print("Arduino Connected")
except Exception as e:
    print("Arduino Not Connected:", e)
    arduino = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('command')
def handle_command(data):
    cmd = data.get('command')
    print(f"[Web Command] Received: {cmd}")

    if arduino:
        try:
            arduino.write((cmd + '\n').encode())
            print("Sent to Arduino:", cmd)
        except Exception as e:
            print("Serial Write Error:", e)
    else:
        print("Arduino not connected")

def open_browser():
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    webbrowser.open(f"http://{local_ip}:5000")

if __name__ == '__main__':
    threading.Thread(target=open_browser, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)