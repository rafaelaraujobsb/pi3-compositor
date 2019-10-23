from flask import request
from flask_restful import Resource

from compositor.rotas.resposta_api import RespostaApi
from compositor.modulo.curadoria import atualizar_frase, lote_validacao


class Curadoria(Resource):
    def get(self, curador):
        try:
            p_concluido, frases, total = lote_validacao(curador)

            return RespostaApi.resposta({'p_concluido': p_concluido, 'frases': frases, 'total': total})
        except Exception as error:
            return RespostaApi.error(str(error))

    def post(self, curador):
        json = request.json

        try:
            atualizar_frase(json['_id'], curador, json['voto'])

            return RespostaApi.sucesso()
        except Exception as error:
            return RespostaApi.error(str(error))
