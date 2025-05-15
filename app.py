# This file is kept for backward compatibility
# The application now uses the factory pattern - see app/__init__.py
from wsgi import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)