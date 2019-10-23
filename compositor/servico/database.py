import gridfs
from bson import ObjectId
from pymongo import MongoClient


from compositor.config import MONGO_DB, MONGO_HOST, MONGO_PWD, MONGO_USER

class ModDatabase:
    """
    Módulo mongo
    """
    def __init__(self, db, user=None, password=None, host='localhost'):
        """
        Faz a conexão com o db.
        """
        if user:
            self.__client = MongoClient(f'mongodb+srv://{user}:{password}@{host}/{db}')
        else:
            self.__client = MongoClient(f'mongodb+srv://{host}:{port}/{db}')

        self.__db = self.__client.get_database()
        self.__fs = gridfs.GridFS(self.__db)

    def get_names_collections(self) -> list:
        """
        Busca todas as collections.

        :return: lista com o nome das collections.
        :rtype: list
        """
        return self.__db.collection_names()

    def get_document(self, collection: str, filter: dict = None, visible: dict = None, max: int = 0,
                     sort: list = [('_id', 1)]) -> list:
        """
        Busca todos os documentos encontrados.

        :param str collection: nome da collection
        :param dict filter: filtro da busca
        :param dict visible: colunas que serão mostradas ou não
        :param int max: quantidade máxima de matches
        :param list sort: | ordenação do resultado (ASCENDING = 1, DESCENDING = -1)
                          | Exemplo: [('_id', 1)]

        :returns: resultado da busca
        :rtype: list
        """

        return [r for r in self.__db[collection].find(filter, visible).sort(sort).limit(max)]

    def get_distinct(self, collection: str, column: str, filter: dict = None) -> tuple:
        """
        Busca todos os dados que são único.

        :param str collection: nome da collection
        :param str column: coluna a ser verificada

        :returns: exemplos unicos e quantas vezes eles se repetem
        :rtype: tuple
        """
        unq = self.__db[collection].distinct(column)

        count = list()
        for r in unq:
            filter[column] = r
            count.append(self.__db[collection].find(filter).count())

        return unq, count

    def __next_id(self, collection: str) -> int:
        """
        Faz a geração de id para substir o objectid.

        :param str collection: nome da collection

        :returns: id sequencial gerado
        :rtype: int
        """

        resultado = self.__db.seqs.find_one_and_update({'_id': collection}, {'$inc': {'id': 1}}, upsert=True)

        if not resultado:
            _id = 1
        else:
            _id = resultado['id'] + 1

        return _id

    def set_document(self, collection: str, value: dict, auto: bool = False) -> int:
        """
        Insere um documento.

        :param str collection: nome da collection
        :param dict value: valor que será inserido
        :param bool auto: ativa o uso de ids

        :returns: id sequencial gerado
        :rtype: int

        .. note::
            Ao usar `auto` como True será usadao um int sequencial como _id.
        """
        if auto:
            value['_id'] = self.__next_id(collection)

        return self.__db[collection].insert_one(value).inserted_id

    def update_document(self, collection: str, filter: dict, value: dict) -> int:
        """
        Altera um ou mais documentos.

        :param str collection: nome da collection
        :param dict filter: filtro da busca
        :param dict value: alteração a ser realizada

        :returns: quantidade de arquivos alterado
        :rtype: int

        .. note::
            `value` não precisa conter `$set`
        """

        if not any(map(value.get, ['$inc', '$set'])):
            value = {'$set': value}

        result = self.__db[collection].update_many(filter, value)

        return result.modified_count

    def len_collection(self, collection: str, filter: dict = None) -> int:
        """
        Quando dados existem de acordo com o filtro

        :param str collection: nome da collection
        :param dict filter: filtro da busca

        :returns: quantidade de registros
        :rtype: int
        """
        return self.__db[collection].find(filter).count()

    def drop_collection(self, collection: str) -> None:
        """
        Deleta uma collection

        :param str collection: nome da collection
        """
        self.__db[collection].drop()
        self.__db.seqs.delete_one({'_id': collection})

    def set_file(self, file: str, filename: str = None) -> str:
        """
        Salva um arquivo usando o GridFs.

        :param file str: file pode ser uma string ou bytes.

        :return: objectid do gridfs
        :rtype: str
        """
        if type(file) == str:
            file = file.encode()

        return str(self.__fs.put(file, filename=filename))

    def get_file(self, objectid: str) -> bytes:
        """
        Busca um arquivo salvo no GridFs.

        :param objectid str: ObjectID do GridFS

        :return: Documento salvo
        :rtype: bytes
        """
        return self.__fs.get(ObjectId(objectid)).read()

    def drop_database(self, db: str) -> None:
        """
        Deleta um databse

        :param db str: nome do database
        """
        self.__client.drop_database(db)

    def __del__(self):
        """
        Encerra a conexão quando o objeto é destruído.
        """
        self.__client.close()



class Database(ModDatabase):
    def __init__(self):
        super().__init__(MONGO_DB, MONGO_USER, MONGO_PWD, MONGO_HOST)
