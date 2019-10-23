from flask import request
from flask_restful import Resource

from compositor.rotas.resposta_api import RespostaApi
from compositor.modulo.curadoria import atualizar_frase, lote_validacao


class Curadoria(Resource):
    def get(self, curador):
        p_concluido, frases = lote_validacao(curador)
        
        return RespostaApi.resposta({'p_concluido': p_concluido, 'frases': frases})


    def post(self, curador):
        json = request.json
        atualizar_frase(json['_id'], curador, json['voto'])

        return RespostaApi.sucesso()
