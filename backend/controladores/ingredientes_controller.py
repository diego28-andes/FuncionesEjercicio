from flask_restful import Resource
from modelos.ingredientes_servicio import IngredientesServicio


class IngredientesController(Resource):
    def get(self):
        return IngredientesServicio().obtener_todos_los_ingredientes()

    def delete(self,ingrediente_id:int):
        (status,mensaje) = IngredientesServicio().eliminar_ingrediente(ingrediente_id)
        if(status != 200):
            return {"error":mensaje}, status
        return {"mensaje":mensaje}, status