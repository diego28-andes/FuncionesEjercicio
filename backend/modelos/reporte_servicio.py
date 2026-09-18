from sqlalchemy import func
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
        if total_recetas == 0:
            raise ValueError("No hay recetas en el sistema")
        return total_recetas

    def obtener_reporte_total_ingredientes(self) -> int:
        session = Session()
        total_ingredientes = session.query(Ingrediente).count()
        if total_ingredientes == 0:
            raise ValueError("No hay ingredientes en el sistema")
        return total_ingredientes
    
    def obtener_reporte_ingrediente_mas_popular(self) -> str:
        session = Session()
        ingrediente_id = session.query(Receta).group_by(Receta.ingrediente_id).order_by(func.count(Receta.id).desc()).first().id        
        ingrediente_mas_popular = session.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()        
        session.close()
        return ingrediente_mas_popular.nombre
        
    

    def obtener_reporte_ingredientes_receta_popular(self) -> list[dict]:
        session = Session()
        ingredientes = session.query(Ingrediente).all()
        if not ingredientes:
            raise ValueError("No hay ingredientes en el sistema")

        reporte = []
        for ingrediente in ingredientes:
            recetas = session.query(Receta).filter(Receta.ingrediente_id == ingrediente.id).all()
            if recetas:
                promedio = sum((receta.tiempo_preparacion or 0) for receta in recetas) / len(recetas)
            else:
                promedio = 0.0
            reporte.append({
                "ingrediente": {
                    "id": ingrediente.id,
                    "nombre": ingrediente.nombre,
                    "tipo": ingrediente.tipo,
                },
                "totalRecetas": len(recetas),
                "promedio": float(promedio),
            })
        return reporte