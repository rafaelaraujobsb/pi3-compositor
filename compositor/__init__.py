from time import time

from loguru import logger
from flasgger import Swagger
from flask import Flask, request

from compositor.rotas import api_bp
from compositor.web import web_index


__version__ = '0.1.0'


logger.add("compositor.log", level='INFO', rotation="500 MB")

# logger.level("REQS", no=38, color="<yellow>")
# logger.add("", level='REQS', rotation="500 MB")

template = {
    "swagger": "2.0",
    "info": {
        "title": "",
        "description": "",
        "version": __version__
    },
}


def start_timer():
    request.start_time = time()


def stop_timer(response):
    resp_time = time() - request.start_time
    logger.info(f"Tempo de resposta: {resp_time}s")

    return response


def record_request_data(response):
    info = f"{request.method} - {request.path} - {response.status_code}"

    logger.info(info)
    # logger.log('REQS', request.json)

    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)


def criar_app():
    app = Flask(__name__)
    Swagger(app, template=template)

    app.register_blueprint(api_bp, url_prefix='/api')
    setup_metrics(app)
    web_index(app)

    return app
