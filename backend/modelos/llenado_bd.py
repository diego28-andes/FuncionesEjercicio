from modelos.recetas import Receta
from modelos.ingredientes import Ingrediente
from modelos.base_declarativa import Session, engine, Base

Base.metadata.create_all(engine)

session = Session()

#Agregar ingredientes

Pollo = Ingrediente(nombre='Pollo',tipo='Carne',unidad_medida='kg',disponible=True)
Cebolla = Ingrediente(nombre='Cebolla',tipo='Vegetal',unidad_medida='lb',disponible=True)
Tomate = Ingrediente(nombre='Tomate',tipo='Vegetal',unidad_medida='lb',disponible=True)
Arroz = Ingrediente(nombre='Arroz',tipo='Granos',unidad_medida='lb',disponible=True)
session.add(Pollo)
session.add(Cebolla)
session.add(Tomate)
session.add(Arroz)
session.commit()

#Agregar recetas
Pollo_cebolla = Receta(nombre='Pollo con cebolla',descripcion='Pollo con cebolla',dificultad='Facil',tiempo_preparacion=30,porciones=4,ingrediente_id=Pollo.id)
cebolla_española = Receta(nombre='Cebolla española',descripcion='Cebolla española',dificultad='Facil',tiempo_preparacion=50,porciones=6,ingrediente_id=Cebolla.id)
bolognesa = Receta(nombre='Bolognesa',descripcion='Bolognesa',dificultad='Media',tiempo_preparacion=60,porciones=8,ingrediente_id=Tomate.id)
arroz_con_pollo = Receta(nombre='Arroz con pollo',descripcion='Arroz con pollo',dificultad='Facil',tiempo_preparacion=20,porciones=4,ingrediente_id=Arroz.id)
session.add(Pollo_cebolla)
session.add(cebolla_española)
session.add(bolognesa)
session.add(arroz_con_pollo)
session.commit()
