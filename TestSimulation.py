import os
from flask import Flask
from keras.models import load_model
from socketIO_client import SocketIO

# Suppress TensorFlow logging messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

# Initialize Flask app
app = Flask(__name__)

# Connect to the server at http://localhost:4567
socketio = SocketIO('http://localhost', 4567, async_mode="threading")

# Maximum speed
maxSpeed = 10

# Preprocess function for image
def preProcess(img):
    img = img[60:135, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

# Callback function to handle telemetry data
@socketio.on('telemetry')
def telemetry(data):
    speed = float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = preProcess(image)
    image = np.array([image])
    steering = float(model.predict(image))
    throttle = 1.0 - speed / maxSpeed
    print('{} {} {}'.format(steering, throttle, speed))
    sendControl(steering, throttle)

# Callback function to handle connection event
@socketio.on('connect')
def connect():
    print('Connected')
    sendControl(0, 0)

# Function to send control commands
def sendControl(steering, throttle):
    socketio.emit('steer', {
        'steering_angle': str(steering),
        'throttle': str(throttle)
    })

if __name__ == '__main__':
    # Load the trained model
    model = load_model('model.h5')
    # Run the SocketIO app
    socketio.run(app)
