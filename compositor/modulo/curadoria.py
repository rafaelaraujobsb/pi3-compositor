from time import sleep

from compositor.servico.database import Database
from compositor.config import DATABASE


def lote_validacao(curador):
    db = Database()
    frases = db.get_document('curadoria', {'curador': curador, 'status': 0}, max=10)
    qtd = db.get_document('curador', {'_id': curador}, {'_id': 0})[0]
    prc_feito = (qtd['curado'] / qtd['curar']) * 100
    # frases = DATABASE['curadoria']
    # qtd = DATABASE['curador'][0]
    # prc_feito = (qtd['curado'] / qtd['curar']) * 100
    # sleep(2)

    return prc_feito, frases, qtd['curar']


def atualizar_frase(id_frase, curador, voto):
    dados = {'$set': {'status': voto}}

    if voto == 1:
        dados['$inc'] = {'votos': 1}

    db = Database()
    db.update_document('curadoria', {'_id': id_frase}, dados)
    db.update_document('curador', {'_id': curador}, {'$inc': {'curado': 1}})
