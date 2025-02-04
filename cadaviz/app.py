from apps import app  # ✅ Import Dash instance from __init__.py
from apps.layout import layout  # ✅ Correct import
from apps.callbacks import register_callbacks  # ✅ Use register_callbacks(app)

# ✅ Ensure the app layout is set correctly
app.layout = layout

# ✅ Register Callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8050)
