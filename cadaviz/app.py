from apps import app  
from apps.layout import layout  
from apps.callbacks import register_callbacks  

app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8050)
