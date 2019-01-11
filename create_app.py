# coding:utf-8
from flask import Flask
from flask_cors import CORS
import config
from my_dispatcher import api
from werkzeug.contrib.fixers import ProxyFix


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api.as_blueprint(url='/api'))
    # 跨域请求
    CORS(app, supports_credentials=True)
    app.config['DEBUG'] = config.DEBUG
    return app


app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)


