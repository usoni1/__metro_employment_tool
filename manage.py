import os, sys
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['SET_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=5005)
