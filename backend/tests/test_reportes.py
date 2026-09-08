import unittest
from unittest.mock import MagicMock, patch

from app import app
from modelos.ingredientes import Ingrediente
from modelos.ingredientes_servicio import IngredientesServicio
from modelos.recetas import Receta
from modelos.recetas_servicio import RecetasServicio
from modelos.reporte_servicio import ReporteServicio


class ReportesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.servicio = ReporteServicio()

    def tearDown(self):
        pass

    def _session_con_ingredientes(self, mock_session_cls, ingredientes_y_recetas):
        """Arma un Session falso: lista de (nombre, cantidad_recetas)."""
        ingredientes = []
        recetas_por_id = {}
        for indice, (nombre, cantidad) in enumerate(ingredientes_y_recetas, start=1):
            ingrediente = MagicMock()
            ingrediente.id = indice
            ingrediente.nombre = nombre
            ingredientes.append(ingrediente)
            recetas_por_id[indice] = [MagicMock() for _ in range(cantidad)]

        session = mock_session_cls.return_value
        query_ingredientes = MagicMock()
        query_ingredientes.all.return_value = ingredientes
        query_ingredientes.count.return_value = len(ingredientes)
        query_ingredientes.order_by.return_value.first.return_value = (
            ingredientes[0] if ingredientes else None
        )

        query_recetas = MagicMock()
        query_recetas.filter.side_effect = self._filtros_en_orden(recetas_por_id)
        query_recetas.count.return_value = sum(len(r) for r in recetas_por_id.values())

        def query_side_effect(model):
            if model is Ingrediente:
                return query_ingredientes
            if model is Receta:
                return query_recetas
            return MagicMock()

        session.query.side_effect = query_side_effect
        return session

    def _filtros_en_orden(self, recetas_por_id):
        ids = list(recetas_por_id.keys())
        estado = {"indice": 0}

        def filter_side_effect(*_args, **_kwargs):
            consulta = MagicMock()
            ingrediente_id = ids[estado["indice"]]
            estado["indice"] += 1
            recetas = recetas_por_id[ingrediente_id]
            consulta.all.return_value = recetas
            consulta.count.return_value = len(recetas)
            return consulta

        return filter_side_effect

#region pruebas HTTP del reporte de popularidad
    def test_obtener_reporte_ingredientes_por_popularidad(self):
        response = self.client.get("/api/reportes/ingredientes-por-popularidad")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        for ingrediente in response.json:
            self.assertIn("ingrediente", ingrediente)
            self.assertIn("cantidad_recetas", ingrediente)
            self.assertIsInstance(ingrediente["cantidad_recetas"], int)
            self.assertGreater(ingrediente["cantidad_recetas"], 0)
            self.assertIsInstance(ingrediente["ingrediente"], str)
            self.assertNotEqual(ingrediente["ingrediente"], "")

    def test_endpoint_popularidad_inexistente_retorna_404(self):
        response = self.client.get("/api/reportes/ingredientes-por-popularidade")
        self.assertEqual(response.status_code, 404)

    def test_endpoint_popularidad_no_acepta_post(self):
        response = self.client.post("/api/reportes/ingredientes-por-popularidad")
        self.assertIn(response.status_code, (404, 405))
#endregion

#region pruebas HTTP de totales y mas popular
    def test_obtener_reporte_total_recetas(self):
        response = self.client.get("/api/reportes/total-recetas")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, int)
        self.assertGreater(response.json, 0)

    def test_obtener_reporte_total_ingredientes(self):
        response = self.client.get("/api/reportes/total-ingredientes")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, int)
        self.assertGreater(response.json, 0)

    def test_obtener_reporte_ingrediente_mas_popular(self):
        response = self.client.get("/api/reportes/ingrediente-mas-popular")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, str)
        self.assertNotEqual(response.json, "")

    def test_endpoint_total_recetas_inexistente_retorna_404(self):
        response = self.client.get("/api/reportes/total-receta")
        self.assertEqual(response.status_code, 404)
#endregion

#region pruebas del servicio: contrato y consistencia con la bd
    def test_servicio_popularidad_retorna_lista_con_claves_esperadas(self):
        reporte = self.servicio.obtener_reporte_ingredientes_por_popularidad()
        self.assertIsInstance(reporte, list)
        self.assertGreater(len(reporte), 0)
        for item in reporte:
            self.assertEqual(set(item.keys()), {"ingrediente", "cantidad_recetas"})
            self.assertIsInstance(item["ingrediente"], str)
            self.assertNotEqual(item["ingrediente"], "")
            self.assertIsInstance(item["cantidad_recetas"], int)
            self.assertGreaterEqual(item["cantidad_recetas"], 0)

    def test_servicio_popularidad_no_repite_ingredientes(self):
        reporte = self.servicio.obtener_reporte_ingredientes_por_popularidad()
        nombres = [item["ingrediente"] for item in reporte]
        self.assertEqual(len(nombres), len(set(nombres)))

    def test_suma_de_recetas_del_reporte_igual_al_total_de_recetas(self):
        reporte = self.servicio.obtener_reporte_ingredientes_por_popularidad()
        total_en_reporte = sum(item["cantidad_recetas"] for item in reporte)
        total_recetas = self.servicio.obtener_reporte_total_recetas()
        self.assertEqual(total_en_reporte, total_recetas)

    def test_total_recetas_coincide_con_el_listado_de_recetas(self):
        total = self.servicio.obtener_reporte_total_recetas()
        recetas = RecetasServicio().obtener_todas_las_recetas()
        self.assertEqual(total, len(recetas))
        self.assertGreater(total, 0)

    def test_total_ingredientes_coincide_con_el_listado_de_ingredientes(self):
        total = self.servicio.obtener_reporte_total_ingredientes()
        ingredientes = IngredientesServicio().obtener_todos_los_ingredientes()
        self.assertEqual(total, len(ingredientes))
        self.assertGreater(total, 0)

    def test_mas_popular_es_un_ingrediente_del_reporte(self):
        reporte = self.servicio.obtener_reporte_ingredientes_por_popularidad()
        nombres = [item["ingrediente"] for item in reporte]
        mas_popular = self.servicio.obtener_reporte_ingrediente_mas_popular()
        self.assertIn(mas_popular, nombres)

    def test_mas_popular_es_el_de_mas_recetas(self):
        reporte = self.servicio.obtener_reporte_ingredientes_por_popularidad()
        esperado = max(reporte, key=lambda item: item["cantidad_recetas"])["ingrediente"]
        actual = self.servicio.obtener_reporte_ingrediente_mas_popular()
        self.assertEqual(actual, esperado)
#endregion

#region pruebas del servicio con datos controlados (mocks)
    @patch("modelos.reporte_servicio.Session")
    def test_popularidad_lista_vacia_cuando_no_hay_ingredientes(self, mock_session_cls):
        self._session_con_ingredientes(mock_session_cls, [])
        reporte = ReporteServicio().obtener_reporte_ingredientes_por_popularidad()
        self.assertEqual(reporte, [])

    @patch("modelos.reporte_servicio.Session")
    def test_popularidad_incluye_ingrediente_sin_recetas(self, mock_session_cls):
        self._session_con_ingredientes(mock_session_cls, [("Azafran", 0)])
        reporte = ReporteServicio().obtener_reporte_ingredientes_por_popularidad()
        self.assertEqual(len(reporte), 1)
        self.assertEqual(reporte[0]["ingrediente"], "Azafran")
        self.assertEqual(reporte[0]["cantidad_recetas"], 0)

    @patch("modelos.reporte_servicio.Session")
    def test_popularidad_ordenada_de_mayor_a_menor(self, mock_session_cls):
        self._session_con_ingredientes(
            mock_session_cls,
            [("Tomate", 1), ("Pollo", 3), ("Azafran", 0)],
        )
        reporte = ReporteServicio().obtener_reporte_ingredientes_por_popularidad()
        cantidades = [item["cantidad_recetas"] for item in reporte]
        self.assertEqual(cantidades, sorted(cantidades, reverse=True))
        self.assertEqual(reporte[0]["ingrediente"], "Pollo")
        self.assertEqual(reporte[0]["cantidad_recetas"], 3)

    @patch("modelos.reporte_servicio.Session")
    def test_total_recetas_es_cero_si_no_hay_recetas(self, mock_session_cls):
        self._session_con_ingredientes(mock_session_cls, [])
        total = ReporteServicio().obtener_reporte_total_recetas()
        self.assertEqual(total, 0)

    @patch("modelos.reporte_servicio.Session")
    def test_total_ingredientes_es_cero_si_no_hay_ingredientes(self, mock_session_cls):
        self._session_con_ingredientes(mock_session_cls, [])
        total = ReporteServicio().obtener_reporte_total_ingredientes()
        self.assertEqual(total, 0)

    @patch("modelos.reporte_servicio.Session")
    def test_mas_popular_con_conteos_distintos(self, mock_session_cls):
        self._session_con_ingredientes(
            mock_session_cls,
            [("Tomate", 1), ("Pollo", 3)],
        )
        mas_popular = ReporteServicio().obtener_reporte_ingrediente_mas_popular()
        self.assertEqual(mas_popular, "Pollo")

    @patch("modelos.reporte_servicio.Session")
    def test_mas_popular_sin_ingredientes_lanza_error_claro(self, mock_session_cls):
        self._session_con_ingredientes(mock_session_cls, [])
        try:
            ReporteServicio().obtener_reporte_ingrediente_mas_popular()
        except AttributeError:
            self.fail("Sin ingredientes debe lanzar ValueError, no AttributeError")
        except ValueError as error:
            self.assertIn("ingrediente", str(error).lower())
            return
        self.fail("Se esperaba ValueError cuando no hay ingredientes")
#endregion
