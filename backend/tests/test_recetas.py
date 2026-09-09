import random
import unittest
from unittest.mock import MagicMock
from app import app
from modelos.enums import DIFICULTADES, NOMBRES_RECETAS
from modelos.recetas import Receta
from modelos.recetas_servicio import RecetasServicio
from modelos.ingredientes_servicio import IngredientesServicio
from modelos.ingredientes import Ingrediente
from modelos.base_declarativa import Session
from faker import Faker



class RecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.servicio = RecetasServicio()
        self.session = Session()
        self.faker = Faker()
        Faker.seed(1000)

        self.recetas = []
        self.recetas_ids = []
        ingredientes = IngredientesServicio().obtener_todos_los_ingredientes()        
        for i in range(10):
            dato = (
                self.faker.unique.word(ext_word_list=NOMBRES_RECETAS),
                self.faker.sentence(ext_word_list=NOMBRES_RECETAS),
                random.choice(ingredientes)["id"],
                self.faker.word(ext_word_list=DIFICULTADES),
            )
            self.recetas_ids.append(dato)
            receta = Receta(
                nombre=dato[0],
                descripcion=dato[1],
                tiempo_preparacion=random.randint(10, 120),
                porciones=random.randint(1, 10),
                ingrediente_id=dato[2],
                dificultad=dato[3],
            )
            self.recetas.append(receta)
            self.session.add(receta)
        self.session.commit()

    def tearDown(self):        
        pass 

#region pruebas del endpoint que retorna todas las recetas
    def test_obtener_todas_las_recetas(self):
        recetas = RecetasServicio().obtener_todas_las_recetas()
        self.assertGreater(len(recetas), 0)
    
    def test_endpoint_recetas_retorna_200_y_lista(self):
        response = self.client.get("/api/recetas")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
#endregion

#region pruebas del metodo de creacion de recetas
    def test_crear_receta_sin_nombre_lanza_error(self):
        receta_mock = MagicMock(spec=Receta)
        receta_mock.nombre = None
        receta_mock.ingrediente_id = 1

        with self.assertRaises(ValueError) as error:
            RecetasServicio().crear_receta(receta_mock)

        self.assertEqual(str(error.exception), "El nombre de la receta es requerido")

    def test_endpoint_crear_receta_sin_nombre(self):
        receta_mock = MagicMock(spec=Receta)
        receta_mock.nombre = "prueba con nombre"
        receta_mock.ingrediente_id = None
        with self.assertRaises(ValueError) as error:
            RecetasServicio().crear_receta(receta_mock)
        self.assertEqual(str(error.exception), "El ingrediente principal es requerido")

    def test_endpoint_crear_receta_nombre_no_pueded_repetirse(self):
        receta_mock = MagicMock(spec=Receta)
        receta_mock.nombre = "Arroz con pollo"
        receta_mock.ingrediente_id = 1
        with self.assertRaises(ValueError) as error:
            RecetasServicio().crear_receta(receta_mock)
        self.assertEqual(str(error.exception), "El nombre de la receta ya existe")
#endregion

