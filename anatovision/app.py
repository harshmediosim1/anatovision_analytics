from apps import app, server
from apps.layout import Main_layout
from apps.callbacks import register_callbacks
from apps.socket_manager import socketio

app.layout = Main_layout
register_callbacks(app)

if __name__ == '__main__':
    socketio.run(server, debug=True, host="0.0.0.0", port=8050)
