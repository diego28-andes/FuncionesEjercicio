
from modelos.ingredientes import Ingrediente
from modelos.base_declarativa import Session
from modelos.recetas import Receta


class RecetasServicio:
    def obtener_todas_las_recetas(self) -> list[dict]:
        session = Session()
        recetas_bd = session.query(Receta).all()               
        recetas_con_ingrediente = []
        for receta in recetas_bd:                           
            ingrediente = session.query(Ingrediente).filter(Ingrediente.id == receta.ingrediente_id).first()  
            receta_completa = {
            "id": receta.id,
            "nombre": receta.nombre,
            "descripcion": receta.descripcion,
            "tiempo_preparacion": receta.tiempo_preparacion,
            "dificultad": receta.dificultad,
            "porciones": receta.porciones,
            "ingrediente_nombre": ingrediente.nombre,
        }
            recetas_con_ingrediente.append(receta_completa)
        return recetas_con_ingrediente

    def crear_receta(self, receta: Receta) -> Receta:
        nombre = self.validar_nombre(receta)
        self.validar_ingrediente_principal(receta)
        session = Session()
        self.validar_nombre_unico(session, nombre)
        return self.guardar_receta(session, receta, nombre)

    def validar_nombre(self, receta: Receta) -> str:
        if receta.nombre is None or not str(receta.nombre).strip():
            raise ValueError("El nombre de la receta es requerido")
        return str(receta.nombre).strip()

    def validar_ingrediente_principal(self, receta: Receta) -> None:
        if receta.ingrediente_id is None:
            raise ValueError("El ingrediente principal es requerido")

    def validar_nombre_unico(self, session, nombre: str) -> None:
        receta_existente = session.query(Receta).filter(Receta.nombre == nombre).first()
        if receta_existente:
            raise ValueError("El nombre de la receta ya existe")

    def guardar_receta(self, session, receta: Receta, nombre: str) -> Receta:
        nueva_receta = Receta(
            nombre=nombre,
            descripcion=getattr(receta, "descripcion", None),
            tiempo_preparacion=getattr(receta, "tiempo_preparacion", None),
            dificultad=getattr(receta, "dificultad", None),
            porciones=getattr(receta, "porciones", None),
            ingrediente_id=receta.ingrediente_id,
        )
        session.add(nueva_receta)
        session.commit()
        session.refresh(nueva_receta)
        return nueva_receta