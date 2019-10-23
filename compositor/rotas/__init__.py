from flask import Blueprint
from flask_restful import Api

from compositor.rotas.curadoria import Curadoria


api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)


api.add_resource(Curadoria, '/curador/<string:curador>')
