# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # ルート設定をここに追加
    from .routes import main
    app.register_blueprint(main)

    return app
