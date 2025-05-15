# run_dev.py
from app import create_app
from app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
