# app/routes/__init__.py
from .main import main_bp
from .health import health_bp


def register_blueprints(app):
    """Register all blueprints with the application"""
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
