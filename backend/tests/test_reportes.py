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
            actual = session.get(Receta, receta.id)
            if actual:
                session.delete(actual)
        session.commit()
        for ingrediente in self.ingredientes:
            actual = session.get(Ingrediente, ingrediente.id)
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
    
    def test_ingrediente_mas_popular(self):
        ingrediente = self.servicio.obtener_reporte_ingrediente_mas_popular()
        self.assertIsNotNone(ingrediente)
        self.assertIsInstance(ingrediente, str)
        
    
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


