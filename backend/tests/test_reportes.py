import random
import unittest
from modelos.enums import DIFICULTADES, NOMBRES_INGREDIENTES, NOMBRES_RECETAS, TIPOS_INGREDIENTES, UNIDADES_MEDIDA
from faker import Faker
from app import app
from modelos.base_declarativa import Session
from modelos.ingredientes import Ingrediente
from modelos.recetas import Receta
from modelos.reporte_servicio import ReporteServicio




class ReportesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.servicio = ReporteServicio()
        self.session = Session()
        self.faker = Faker()
        Faker.seed(1000)

        self.ingredientes = []
        self.ingredientes_ids = []
        self.recetas = []
        self.recetas_ids = []

        
        for i in range(10):
            dato = (
                self.faker.unique.word(ext_word_list=NOMBRES_INGREDIENTES),
                self.faker.word(ext_word_list=TIPOS_INGREDIENTES),
                self.faker.word(ext_word_list=UNIDADES_MEDIDA),
                True,
            )
            self.ingredientes_ids.append(dato)
            ingrediente = Ingrediente(
                nombre=dato[0],
                tipo=dato[1],
                unidad_medida=dato[2],
                disponible=dato[3],
            )
            self.ingredientes.append(ingrediente)
            self.session.add(ingrediente)

        self.session.commit()

        
        for i in range(10):
            ingrediente = random.choice(self.ingredientes)
            dato = (
                self.faker.unique.word(ext_word_list=NOMBRES_RECETAS),
                self.faker.sentence(ext_word_list=NOMBRES_RECETAS),
                ingrediente.id,
                self.faker.word(ext_word_list=DIFICULTADES),
            )
            self.recetas_ids.append(dato)
            receta = Receta(
                nombre=dato[0],
                descripcion=dato[1],
                tiempo_preparacion=self.faker.random_int(min=10, max=90),
                dificultad="Facil",
                porciones=self.faker.random_int(min=1, max=8),
                ingrediente_id=dato[2],
            )
            self.recetas.append(receta)
            self.session.add(receta)

        self.session.commit()

    def tearDown(self):
        session = Session()
        for receta in self.recetas:
            receta_id = receta.__dict__.get("id")
            if receta_id is None:
                continue
            actual = session.get(Receta, receta_id)
            if actual:
                session.delete(actual)
        session.commit()
        for ingrediente in self.ingredientes:
            ingrediente_id = ingrediente.__dict__.get("id")
            if ingrediente_id is None:
                continue
            actual = session.get(Ingrediente, ingrediente_id)
            if actual:
                session.delete(actual)
        session.commit()
        session.close()

    def test_contructor(self):
        for ingrediente, dato in zip(self.ingredientes, self.ingredientes_ids):
            self.assertEqual(ingrediente.nombre, dato[0])
            self.assertEqual(ingrediente.tipo, dato[1])
            self.assertEqual(ingrediente.unidad_medida, dato[2])
            self.assertEqual(ingrediente.disponible, dato[3])
        for receta, dato in zip(self.recetas, self.recetas_ids):
            self.assertEqual(receta.nombre, dato[0])
            self.assertEqual(receta.descripcion, dato[1])
            self.assertEqual(receta.ingrediente_id, dato[2])


    def test_obtener_total_recetas_del_sistema(self):
        total = self.servicio.obtener_reporte_total_recetas()    
        self.assertGreaterEqual(total, len(self.recetas))

    def test_obtener_total_ingredientes_del_sistema(self):
        total = self.servicio.obtener_reporte_total_ingredientes()
        self.assertGreaterEqual(total, len(self.ingredientes))
    
    def test_total_ingredientes_es_entero(self):
        total = self.servicio.obtener_reporte_total_ingredientes()
        self.assertIsInstance(total, int)
    
    def test_total_recetas_es_entero(self):
        total = self.servicio.obtener_reporte_total_recetas()
        self.assertIsInstance(total, int)

    def test_total_recetas_sin_recetas_lanza_error(self):
        nombres_del_setup = {receta.nombre for receta in self.recetas}
        recetas_backup = [
            {
                "nombre": receta.nombre,
                "descripcion": receta.descripcion,
                "tiempo_preparacion": receta.tiempo_preparacion,
                "dificultad": receta.dificultad,
                "porciones": receta.porciones,
                "ingrediente_id": receta.ingrediente_id,
            }
            for receta in self.session.query(Receta).all()
        ]

        self.session.query(Receta).delete()
        self.session.commit()

        try:
            with self.assertRaises(ValueError) as error:
                self.servicio.obtener_reporte_total_recetas()
            self.assertEqual(str(error.exception), "No hay recetas en el sistema")
        finally:
            for dato in recetas_backup:
                self.session.add(Receta(**dato))
            self.session.commit()
            self.recetas = [
                receta
                for receta in self.session.query(Receta).all()
                if receta.nombre in nombres_del_setup
            ]

    def test_total_ingredientes_sin_ingredientes_lanza_error(self):
        self.recetas = []
        self.ingredientes = []
        self.session.query(Receta).delete()
        self.session.query(Ingrediente).delete()
        self.session.commit()

        with self.assertRaises(ValueError) as error:
            self.servicio.obtener_reporte_total_ingredientes()
        self.assertEqual(str(error.exception), "No hay ingredientes en el sistema")
    
    def test_total_ingredientes_aumenta_al_agregar_uno(self):
            total_antes = self.servicio.obtener_reporte_total_ingredientes()

            nuevo = Ingrediente(
                nombre=self.faker.unique.word(ext_word_list=NOMBRES_INGREDIENTES),
                tipo="Vegetal",
                unidad_medida="kg",
                disponible=True,
            )
            self.session.add(nuevo)
            self.session.commit()
            self.ingredientes.append(nuevo)

            total_despues = self.servicio.obtener_reporte_total_ingredientes()
            self.assertEqual(total_despues, total_antes + 1)


    def test_total_ingredientes_disminuye_al_eliminar_uno(self):
        total_antes = self.servicio.obtener_reporte_total_ingredientes()
        ingrediente = random.choice(self.ingredientes)
        self.session.delete(ingrediente)
        self.session.commit()
        self.ingredientes.remove(ingrediente)
        total_despues = self.servicio.obtener_reporte_total_ingredientes()
        self.assertEqual(total_despues, total_antes - 1)

    def total_recetas_aumenta_al_agregar_uno(self):
        total_antes = self.servicio.obtener_reporte_total_recetas()
        receta = Receta(
            nombre=self.faker.unique.word(ext_word_list=NOMBRES_RECETAS),
            descripcion=self.faker.sentence(ext_word_list=NOMBRES_RECETAS),
            ingrediente_id=random.choice(self.ingredientes_ids),
            dificultad="Facil",
        )
        self.session.add(receta)
        self.session.commit()
        self.recetas.append(receta)
        total_despues = self.servicio.obtener_reporte_total_recetas()
        self.assertEqual(total_despues, total_antes + 1)

    def total_recetas_disminuye_al_eliminar_uno(self):
        total_antes = self.servicio.obtener_reporte_total_recetas()
        receta = random.choice(self.recetas)
        self.session.delete(receta)
        self.session.commit()
        self.recetas.remove(receta)
        total_despues = self.servicio.obtener_reporte_total_recetas()
        self.assertEqual(total_despues, total_antes - 1)
    
    def test_reporte_ingredientes_receta_popular(self):
        obtener_reporte_ingredientes_receta_popular = self.servicio.obtener_reporte_ingredientes_receta_popular()
        self.assertIsNotNone(obtener_reporte_ingredientes_receta_popular)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular, list)
        self.assertGreaterEqual(len(obtener_reporte_ingredientes_receta_popular), 3)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular[0], dict)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular[0]["ingrediente"], dict)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular[0]["ingrediente"]["id"], int)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular[0]["ingrediente"]["nombre"], str)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular[0]["ingrediente"]["tipo"], str)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular[0]["totalRecetas"], int)
        self.assertIsInstance(obtener_reporte_ingredientes_receta_popular[0]["promedio"], float)

    def test_reporte_calcula_total_y_promedio_de_un_ingrediente(self):
        ingrediente = Ingrediente(
            nombre="Aji criollo",
            tipo="Vegetal",
            unidad_medida="g",
            disponible=True,
        )
        self.session.add(ingrediente)
        self.session.commit()
        self.ingredientes.append(ingrediente)

        for indice, tiempo in enumerate((10, 20, 30)):
            receta = Receta(
                nombre=f"Salsa de aji {indice}",
                descripcion="Receta de control para el promedio",
                tiempo_preparacion=tiempo,
                dificultad="Facil",
                porciones=2,
                ingrediente_id=ingrediente.id,
            )
            self.session.add(receta)
            self.recetas.append(receta)
        self.session.commit()

        reporte = self.servicio.obtener_reporte_ingredientes_receta_popular()
        item = next(
            fila for fila in reporte
            if fila["ingrediente"]["id"] == ingrediente.id
        )

        self.assertEqual(item["totalRecetas"], 3)
        self.assertEqual(item["promedio"], 20.0)

    def test_reporte_sin_ingredientes_lanza_error(self):
        self.recetas = []
        self.ingredientes = []
        self.session.query(Receta).delete()
        self.session.query(Ingrediente).delete()
        self.session.commit()

        with self.assertRaises(ValueError) as error:
            self.servicio.obtener_reporte_ingredientes_receta_popular()
        self.assertEqual(str(error.exception), "No hay ingredientes en el sistema")

    def test_ingrediente_mas_popular(self):
        ingrediente = self.servicio.obtener_reporte_ingrediente_mas_popular()
        self.assertIsNotNone(ingrediente)
        self.assertIsInstance(ingrediente, str)
        
    
  
