
from modelos.recetas import Receta
from flask import request
from modelos.recetas_servicio import RecetasServicio 
from flask_restful import Resource

class RecetasController(Resource):
    def get(self):
        recetas = RecetasServicio().obtener_todas_las_recetas()
        return  recetas
    
    def post(self):
        datos = request.get_json(silent=True) or {}
        receta = Receta(
            nombre=datos.get("nombre"),
            descripcion=datos.get("descripcion"),
            tiempo_preparacion=datos.get("tiempo_preparacion"),
            dificultad=datos.get("dificultad"),
            porciones=datos.get("porciones"),
            ingrediente_id=datos.get("ingrediente_id"),
        )
        try:
            RecetasServicio().crear_receta(receta)
        except ValueError as error:
            return {"error": str(error)}, 400
        return {"mensaje": "Receta validada", "nombre": receta.nombre}, 201