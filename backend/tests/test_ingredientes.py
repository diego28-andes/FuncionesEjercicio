from app import app
import unittest
from modelos.ingredientes_servicio import IngredientesServicio

class IngredientesTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
    
    def tearDown(self):
        pass


    #region pruebas del endpoint que retorna todos los ingredientes
    def test_obtener_todos_los_ingredientes(self):
        ingredientes = IngredientesServicio().obtener_todos_los_ingredientes()
        self.assertGreater(len(ingredientes), 0)
    
    #endregion