from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np
import cv2
import io

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('frame')
def handle_frame(data):
    # Decode the incoming frame
    frame = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Example processing: convert to grayscale
    # processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = 'Processed Video'
    position = (50, 50)  # Text position (x, y)
    font_scale = 1
    font_color = (0, 255, 0)  # Text color (Green in BGR)
    thickness = 2
    cv2.putText(frame, text, position, font, font_scale, font_color, thickness, cv2.LINE_AA)

    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply a color map to the grayscale frame
    color_mapped_frame = cv2.applyColorMap(grayscale_frame, cv2.COLORMAP_JET)

    
    _, buffer = cv2.imencode('.jpg', color_mapped_frame)
    
    # Send back the processed frame
    emit('processed_frame', buffer.tobytes())

if __name__ == '__main__':
    context = ('server.crt', 'server.key')  # Paths to your certificate and key files
    socketio.run(app, host='0.0.0.0', port=4000, ssl_context=context)
