from modelos.base_declarativa import Session
from modelos.ingredientes import Ingrediente
from modelos.recetas import Receta


class IngredientesServicio:
    def obtener_todos_los_ingredientes(self) -> list[dict]:
        session = Session()
        ingredientes_bd = session.query(Ingrediente).all()
        ingredientes = []
        for ingrediente in ingredientes_bd:
            cantidad_recetas = (
                session.query(Receta)
                .filter(Receta.ingrediente_id == ingrediente.id)
                .count()
            )
            ingredientes.append({
                "id": ingrediente.id,
                "nombre": ingrediente.nombre,
                "tipo": ingrediente.tipo,
                "unidad_medida": ingrediente.unidad_medida,
                "disponible": ingrediente.disponible,
                "cantidad_recetas": cantidad_recetas,
            })
        return ingredientes
    
    def agregar_ingrediente(self,ingrediente:Ingrediente) -> Ingrediente:
        session = Session()        
        if(ingrediente.nombre is None or ingrediente.nombre == ""):
            raise ValueError("El nombre del ingrediente es requerido")
        if(ingrediente.tipo is None or ingrediente.tipo == ""):
            raise ValueError("El tipo de ingrediente es requerido")
        if(ingrediente.unidad_medida is None or ingrediente.unidad_medida == ""):
            raise ValueError("La unidad de medida del ingrediente es requerida")
        if(ingrediente.disponible is None or ingrediente.disponible == ""):
            raise ValueError("La disponibilidad del ingrediente es requerida")        
        session.add(ingrediente)
        session.commit()
        session.refresh(ingrediente)
        return ingrediente
    

    #region para eliminar ingredientes
    def eliminar_ingrediente(self,ingrediente_id:int) -> (int,str):
        session = Session()
        ingrediente = session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if(ingrediente is None):
            return (404,"El ingrediente no existe")
        tieneReceta = session.query(Receta).filter(Receta.ingrediente_id == ingrediente.id).count() > 0
        if(tieneReceta):
            return (400,"El ingrediente tiene recetas asociadas y no puede ser eliminado")
        session.delete(ingrediente)
        session.commit()
        return (200,"El ingrediente se eliminó correctamente")
    #endregion

    #region para editar ingredientes
    def editar_ingrediente(self, ingrediente_id: int, ingrediente: Ingrediente):
        session = Session()
        ingrediente_bd = session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()

        # test_editar_ingrediente_no_existe
        if ingrediente_bd is None:
            return (404, "El ingrediente no existe")

        # test_editar_ingrediente_sin_nombre_lanza_error
        if ingrediente.nombre is None or ingrediente.nombre == "":
            raise ValueError("El nombre del ingrediente es requerido")

        # test_editar_ingrediente_sin_tipo_lanza_error
        if ingrediente.tipo is None or ingrediente.tipo == "":
            raise ValueError("El tipo de ingrediente es requerido")

        # test_editar_ingrediente_sin_unidad_lanza_error
        if ingrediente.unidad_medida is None or ingrediente.unidad_medida == "":
            raise ValueError("La unidad de medida del ingrediente es requerida")

        # test_editar_ingrediente_con_recetas_asociadas
        tiene_receta = session.query(Receta).filter(Receta.ingrediente_id == ingrediente_bd.id).count() > 0
        if tiene_receta:
            return (400, "El ingrediente tiene recetas asociadas y no puede ser editado")

        # test_editar_ingrediente_correctamente
        ingrediente_bd.nombre = ingrediente.nombre
        ingrediente_bd.tipo = ingrediente.tipo
        ingrediente_bd.unidad_medida = ingrediente.unidad_medida
        ingrediente_bd.disponible = ingrediente.disponible
        session.commit()
        return (200, "El ingrediente se actualizó correctamente")
    #endregion