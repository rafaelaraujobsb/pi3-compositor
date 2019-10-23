from compositor.servico.database import Database


def lote_validacao(curador):
    db = Database()
    frases = db.get_document('curadoria', {'curador': curador, 'status': 0}, max=10)
    qtd = db.get_document('curador', {'_id': curador}, {'_id': 0})[0]
    prc_feito = (qtd['curado'] / qtd['curar']) / 100

    return prc_feito, frases, qtd['curar']


def atualizar_frase(id_frase, curador, voto):
    dados = {'status': voto}

    if voto == 1:
        dados['votos'] = {'$inc': 1}

    db = Database()
    db.update_document('curadoria', {'_id': id_frase}, dados, valor)
    db.update_document('curador', {'_id': curador}, {'curado': {'$inc': 1}})
