import unittest
from unittest.mock import patch, MagicMock
from controllers.heladeria_controler import HeladeriaController
from models.ingrediente import Ingrediente
from models.producto import Producto
from app import *

class TestHeladeria(unittest.TestCase):

    def setUp(self):
        app.app_context().push()

        # Crear ingredientes de prueba
        self.leche = Ingrediente("Leche", 1.5, 42, 50, True)
        self.azucar = Ingrediente("Azúcar", 0.8, 400, 100, True)
        self.vainilla = Ingrediente("Vainilla", 5.0, 20, 10, True)

        # Crear producto de prueba
        self.helado_vainilla = Producto("Helado de Vainilla", 10.0, "copa", self.leche, self.azucar, self.vainilla)

    def test_ingrediente_es_sano(self):
        self.assertTrue(self.leche.es_sano())  # Debe ser sano
        self.assertFalse(self.azucar.es_sano())  # Azúcar no debe ser sano debido a las calorías

    @patch('models.ingrediente.db')
    def test_abastecer_ingrediente(self, mock_db):
        self.vainilla.abastecer(20)
        self.assertEqual(self.vainilla.inventario, 30)
        mock_db.session.commit.assert_called_once()

    @patch('models.ingrediente.db')
    def test_renovar_inventario(self, mock_db):
        self.vainilla.renovar_inventario(15)
        self.assertEqual(self.vainilla.inventario, 25)
        mock_db.session.commit.assert_called_once()

    def test_ingrediente_es_sano(self):
        ingrediente_sano = Ingrediente("Aceitunas", 0.5, 300, 10, True)
        self.assertFalse(ingrediente_sano.es_sano())

    def test_abastecer_con_valores_invalidos(self):
        with self.assertRaises(ValueError):
            self.vainilla.abastecer(-10)
        with self.assertRaises(ValueError):
            self.vainilla.abastecer(0)

    def test_calcular_calorias(self):
        calorias = self.helado_vainilla.calcular_calorias()
        self.assertEqual(calorias, 42 + 400 + 20)  # Suma de calorías de los ingredientes

    def test_calcular_calorias_malteada(self):
        self.helado_vainilla.tipo = "malteada"
        calorias = self.helado_vainilla.calcular_calorias()
        self.assertEqual(calorias, 42 + 400 + 20)  # Sin lógica adicional, igual a las de copa

    def test_calcular_costo(self):
        costo = self.helado_vainilla.calcular_costo()
        self.assertEqual(costo, 1.5 + 0.8 + 5.0)  # Suma de costos de los ingredientes

    def test_calcular_rentabilidad(self):
        rentabilidad = self.helado_vainilla.rentabilidad()
        self.assertEqual(rentabilidad, 10.0 - (1.5 + 0.8 + 5.0))  # Precio público menos costo

    @patch('models.producto.Producto.query.all')
    def test_encontrar_producto_mas_rentable(self, mock_query_all):
        # Crear lista de productos con diferentes rentabilidades
        helado_chocolate = Producto("Helado de Chocolate", 12.0, "copa", self.leche, self.azucar, self.vainilla)
        mock_query_all.return_value = [self.helado_vainilla, helado_chocolate]

        mas_rentable = HeladeriaController.encontrar_producto_mas_rentable()
        self.assertEqual(mas_rentable.nombre, "Helado de Chocolate")  # Helado de Chocolate es más rentable

    def test_rentabilidad_malo(self):
        producto_sin_ganancia = Producto("Producto sin ganancia", 7.3, "copa", self.leche, self.azucar, self.vainilla)
        self.assertEqual(producto_sin_ganancia.rentabilidad(), 0.0)

        producto_perdida = Producto("Producto en pérdida", 7.0, "copa", self.leche, self.azucar, self.vainilla)
        self.assertLess(producto_perdida.rentabilidad(), 0.0)

    @patch('models.producto.Producto.query.filter_by')
    @patch('models.ingrediente.db')
    def test_vender_producto_exitoso(self, mock_db, mock_filter_by):
        # Mockear el producto
        mock_filter_by.return_value.first.return_value = self.helado_vainilla

        mensaje = HeladeriaController.vender_producto("Helado de Vainilla")
        self.assertEqual(mensaje, "¡Vendido!")
        self.assertEqual(self.leche.inventario, 50)
        self.assertEqual(self.azucar.inventario, 99)
        self.assertEqual(self.vainilla.inventario, 9)
        mock_db.session.commit.assert_called_once()

    @patch('models.producto.Producto.query.filter_by')
    def test_vender_producto_sin_inventario(self, mock_filter_by):
        # Mockear el producto
        mock_filter_by.return_value.first.return_value = self.helado_vainilla
        self.vainilla.inventario = 0  # Sin inventario de vainilla

        with self.assertRaises(ValueError) as context:
            HeladeriaController.vender_producto("Helado de Vainilla")
        self.assertEqual(str(context.exception), "¡Oh no! Nos hemos quedado sin Vainilla.")

    @patch('models.producto.Producto.query.filter_by')
    def test_vender_producto_inexistente(self, mock_filter_by):
        mock_filter_by.return_value.first.return_value = None
        with self.assertRaises(ValueError) as context:
            HeladeriaController.vender_producto("Producto Desconocido")
        self.assertEqual(str(context.exception), "Producto 'Producto Desconocido' no encontrado.")

    @patch('models.producto.Producto.query.filter_by')
    def test_vender_producto_con_ingrediente_insuficiente(self, mock_filter_by):
        self.leche.inventario = 1  # Insuficiente para el producto
        mock_filter_by.return_value.first.return_value = self.helado_vainilla

        with self.assertRaises(ValueError) as context:
            HeladeriaController.vender_producto("Helado de Vainilla")
        self.assertEqual(str(context.exception), "¡Oh no! Nos hemos quedado sin Leche.")

    @patch('models.ingrediente.db')
    def test_abastecer_ingredientes_masivo(self, mock_db):
        ingredientes = [self.leche, self.azucar, self.vainilla]
        for ingrediente in ingredientes:
            ingrediente.abastecer(10)
        self.assertEqual(self.leche.inventario, 60)
        self.assertEqual(self.azucar.inventario, 110)
        self.assertEqual(self.vainilla.inventario, 20)

if __name__ == '__main__':
    unittest.main()
