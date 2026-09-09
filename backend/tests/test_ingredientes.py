import random
from app import app
import unittest
from modelos.ingredientes_servicio import IngredientesServicio
from modelos.ingredientes import Ingrediente
from faker import Faker

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

    #region de pruebas para eliminar ingredientes
    def test_eliminar_ingrediente_no_existe(self):
        (status,mensaje) = IngredientesServicio().eliminar_ingrediente(random.randint(100000,200000))
        self.assertEqual(mensaje, "El ingrediente no existe")
        self.assertEqual(status,404)
    
    def test_eliminar_ingrediente_con_recetas_asociadas(self):
        (status,mensaje) = IngredientesServicio().eliminar_ingrediente(1)
        self.assertEqual(mensaje, "El ingrediente tiene recetas asociadas y no puede ser eliminado")
        self.assertEqual(status,400)

    def test_eliminar_ingrediente_correctamente(self):
        faker = Faker()
        ingrediente =  Ingrediente(nombre=faker.unique.word(),tipo=faker.word(),unidad_medida=faker.word(),disponible=True)        
        ingredienteGuardado = IngredientesServicio().agregar_ingrediente(ingrediente)        
        (status,mensaje) = IngredientesServicio().eliminar_ingrediente(ingrediente.id)
        self.assertEqual(mensaje, "El ingrediente se eliminó correctamente")
        self.assertEqual(status,200)
    #endregion