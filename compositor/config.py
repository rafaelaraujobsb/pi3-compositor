import os


MONGO_DB = os.environ['MONGO_DB']
MONGO_PWD = os.environ['MONGO_PWD']
MONGO_USER = os.environ['MONGO_USER']
MONGO_HOST = os.environ['MONGO_HOST']

DATABASE = {
    'curadoria': [
        {'_id': 1, 'curador': 'rafael', 'frase': 'segundos vira, vira, virou', 'votos': 0, 'status': 0},
        {'_id': 2, 'curador': 'rafael', 'frase': 'amor outra noite e outra vez', 'votos': 0, 'status': 0},
        {'_id': 3, 'curador': 'rafael', 'frase': 'vou brindar contigo esse porre de', 'votos': 0, 'status': 0},
        {'_id': 4, 'curador': 'rafael', 'frase': '. de uma saudade que tanto', 'votos': 0, 'status': 0},
        {'_id': 5, 'curador': 'rafael', 'frase': 'apenas lhe desejar felicidade amor é', 'votos': 0, 'status': 0}
    ],
    'curador': [
        {'_id': 'rafael', 'curado': 0, 'curar': 180563}
    ]
}
