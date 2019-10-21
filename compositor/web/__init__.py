from flask import render_template
from modulo.lstm import criar_modelo


modelo = criar_modelo()


def web_index(app):
    @app.route('/')
    def index():
        return '<h1>Teste</h1>'
