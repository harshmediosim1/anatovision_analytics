from apps import app  
from apps.layout import Main_layout
from apps.callbacks import register_callbacks  
from flask_socketio import SocketIO
import eventlet


socketio = SocketIO(app.server, cors_allowed_origins="*")

app.layout = Main_layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8050)
