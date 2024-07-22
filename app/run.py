from app import app
import layouts  # Importing the module to ensure the layouts are loaded
import callbacks  # noqa: F401

if __name__ == '__main__':
    app.run_server(debug=True)
