from flask import render_template

from compositor.modulo.curadoria import lote_validacao


import time
# from modulo.lstm import criar_modelo


# modelo = criar_modelo()

CURADORES = {
    'rafael': '#F6C655',
    'douglas': '#F56CD0',
    'mauricio': '#7BA3F7',
    'victor': '#B988FA'
}


def web_index(app):
    @app.route('/curadoria/<string:curador>')
    def curadoria(curador):
        return render_template('curadoria.html', cbarra=CURADORES[curador])
