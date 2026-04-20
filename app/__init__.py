from flask import Flask


def create_app():
    app = Flask(__name__, template_folder='views', static_folder='../static')

    from app.controllers.livros import livros_bp
    app.register_blueprint(livros_bp)

    return app
