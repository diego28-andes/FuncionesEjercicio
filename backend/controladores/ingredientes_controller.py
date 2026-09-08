from flask_restful import Resource
from modelos.ingredientes_servicio import IngredientesServicio


class IngredientesController(Resource):
    def get(self):
        return IngredientesServicio().obtener_todos_los_ingredientes()