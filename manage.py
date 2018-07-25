import os, sys
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if len(sys.argv) > 1:
        #for server instance
        app.run(host='0.0.0.0', port=port)
    else:
        #for local instance
        app.run(host='127.0.0.1', port=5500)
