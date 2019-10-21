class RespostaApi:

    @staticmethod
    def sucesso():
        return {'message': 'success'}, 200

    @staticmethod
    def resposta(value):
        return {'status': 200, 'results': value}, 200

    @staticmethod
    def json_invalido():
        return {'message': 'JSON inválido!', 'status': 406}, 406

    @staticmethod
    def error(message):
        return {'message': message}, 500

    @staticmethod
    def create_success():
        return {'message': 'success on user creating'}, 201
