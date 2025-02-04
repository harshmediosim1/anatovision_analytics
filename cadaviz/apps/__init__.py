from dash import Dash

# ✅ Initialize Dash App
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Required for deployment (Gunicorn)
