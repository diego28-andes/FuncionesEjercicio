from modelos.base_declarativa import Session
from modelos.ingredientes import Ingrediente
from modelos.recetas import Receta

class ReporteServicio:

    def obtener_reporte_ingredientes_por_popularidad(self) -> list[dict]:
        session = Session()
        ingredientes = session.query(Ingrediente).all()
        reporte = []
        for ingrediente in ingredientes:
            recetas = session.query(Receta).filter(Receta.ingrediente_id == ingrediente.id).all()
            reporte.append({
                "ingrediente": ingrediente.nombre,
                "cantidad_recetas": len(recetas)
            })
        return reporte

    def obtener_reporte_total_recetas(self) -> int:
        session  = Session()
        total_recetas = session.query(Receta).count()
        return total_recetas

    def obtener_reporte_total_ingredientes(self) -> int:
        session = Session()
        total_ingredientes = session.query(Ingrediente).count()
        return total_ingredientes
    
    def obtener_reporte_ingrediente_mas_popular(self) -> str:
        session = Session()
        ingrediente_mas_popular = session.query(Ingrediente).order_by(Ingrediente.nombre).first()
        return ingrediente_mas_popular.nombre
    