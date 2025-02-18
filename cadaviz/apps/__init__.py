from dash import Dash
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

#server.secret_key = secrets.token_hex(16)