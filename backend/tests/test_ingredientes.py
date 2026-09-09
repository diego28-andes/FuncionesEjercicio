import random
import unittest
from modelos.enums import NOMBRES_INGREDIENTES,TIPOS_INGREDIENTES,UNIDADES_MEDIDA
from modelos.base_declarativa import Session
from app import app
from modelos.ingredientes_servicio import IngredientesServicio
from modelos.ingredientes import Ingrediente
from faker import Faker

class IngredientesTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.servicio = IngredientesServicio()
        self.session = Session()
        self.faker = Faker()
        Faker.seed(1000)

        self.ingredientes = []
        self.ingredientes_ids = []
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