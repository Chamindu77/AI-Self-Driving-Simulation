from tensorflow.python.keras.models import load_model
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import socketio
import eventlet.wsgi
import numpy as np
from flask import Flask
import base64
from io import BytesIO
from PIL import Image
import cv2

# FOR REAL TIME COMMUNICATION BETWEEN CLIENT AND SERVER
sio = socketio.Server()
# FLASK IS A MICRO WEB FRAMEWORK WRITTEN IN PYTHON
app = Flask(__name__)

maxSpeed = 1

# Preprocess function for image
def preProcess(img):
    img = img[60:135, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

# Event handler for receiving telemetry data
@sio.on('telemetry')
def telemetry(sid, data):
    speed =10 #float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.array(image)
    image = preProcess(image)
    image = np.array([image])
    steering = float(model.predict(image))
    throttle = 10 #1.0 - speed / maxSpeed
    print(f'{steering}, {throttle}, {speed}')
    sendControl(steering, throttle)

# Event handler for client connection
@sio.on('connect')
def connect(sid, environ):
    print('Connected')
    sendControl(0, 0)

# Function to send control commands to the client
def sendControl(steering, throttle):
    sio.emit('steer', data={
        'steering_angle': steering.__str__(),
        'throttle': throttle.__str__()
    })

if __name__ == '__main__':
    # Load the pre-trained model
    model = load_model('model.h5')

    # Wrap Flask app with SocketIO's middleware
    app = socketio.Middleware(sio, app)

    # Listen to port 4567
    print("Starting server...")
    eventlet.wsgi.server(eventlet.listen(('localhost', 4567)), app)
