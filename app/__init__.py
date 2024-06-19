from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from threading import Lock
import os
from app import telemetry

# Create the Flask app
app = Flask(__name__)

# Create the SocketIO instance
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins='*')  # Enable CORS for all origins
thread = None
thread_lock = Lock()

# On connect, send the dashboard data
@socketio.on('connect')
def handle_connect():
    socketio.emit('data_update', telemetry.get_dashboard_data()) 

# Background thread to emit data updates
def background_thread():
    while True:
        data = telemetry.get_dashboard_data()
        socketio.emit('data_update', data)

# Start the background thread on connect
@socketio.event
def connect():
    global thread
    thread = socketio.start_background_task(background_thread)

# Start the Flask app
if __name__ == '__main__':
    socketio.run(app, host='localhost', port=2567)
