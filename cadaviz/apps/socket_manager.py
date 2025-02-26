from flask_socketio import SocketIO
from apps import app  # Import the Dash app

# Initialize SocketIO
socketio = SocketIO(app.server, cors_allowed_origins="*",async_mode="eventlet")
