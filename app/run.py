from app import app
from layout import layout
import callbacks  # noqa: F401

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)
