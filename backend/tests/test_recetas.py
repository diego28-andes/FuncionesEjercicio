import unittest
from unittest.mock import MagicMock
from app import app
from modelos.recetas import Receta
from modelos.recetas_servicio import RecetasServicio



class RecetaTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

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

