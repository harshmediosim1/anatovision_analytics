from apps import app  
from apps.layout import layout  
from apps.callbacks import register_callbacks  
from flask_socketio import SocketIO
import eventlet


socketio = SocketIO(app.server, cors_allowed_origins="*")

app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    socketio.run(app.server, debug=False, host="0.0.0.0", port=8050 , use_reloader=False)
