import unittest
from unittest.mock import patch, MagicMock
from controllers.heladeria_controler import HeladeriaController
from models.ingrediente import Ingrediente
from models.producto import Producto
from models.heladeria import Heladeria
from app import app

class TestHeladeriaController(unittest.TestCase):
    def setUp(self):
        # Crear ingredientes
        self.ingredientes = {
            1: Ingrediente("Leche", 1.5, 42, 50, True),
            3: Ingrediente("Azúcar", 0.8, 400, 100, True),
            5: Ingrediente("Vainilla", 5.0, 20, 10, True),
            6: Ingrediente("Fresas", 4.0, 35, 15, True),
            7: Ingrediente("Mango", 3.5, 60, 25, True),
            8: Ingrediente("Chocolate", 4.5, 540, 10, True),
            10: Ingrediente("Galletas", 2.0, 500, 40, False),
            16: Ingrediente("Sirope de Fresa", 2.5, 320, 20, True),
            17: Ingrediente("Sirope de Chocolate", 3.0, 340, 25, True),
        }

        # Crear productos
        self.productos = [
            Producto("Helado de Vainilla", 10.0, "copa", self.ingredientes[1], self.ingredientes[3], self.ingredientes[5]),
            Producto("Helado de Chocolate", 12.0, "copa", self.ingredientes[1], self.ingredientes[3], self.ingredientes[8]),
            Producto("Helado de Fresa", 11.0, "copa", self.ingredientes[1], self.ingredientes[3], self.ingredientes[6]),
            Producto("Helado de Mango", 11.5, "copa", self.ingredientes[1], self.ingredientes[3], self.ingredientes[7]),
            Producto("Helado Napolitano", 13.0, "copa", self.ingredientes[1], self.ingredientes[8], self.ingredientes[6]),
            Producto("Sundae de Chocolate", 8.0, "copa", self.ingredientes[1], self.ingredientes[8], self.ingredientes[17]),
            Producto("Milkshake de Fresa", 7.5, "malteada", self.ingredientes[1], self.ingredientes[3], self.ingredientes[16]),
            Producto("Paleta de Frutas", 4.5, "copa", self.ingredientes[6], self.ingredientes[7], self.ingredientes[3]),
            Producto("Torta Helada", 15.0, "copa", self.ingredientes[10], self.ingredientes[5], self.ingredientes[8]),
            Producto("Cono Clásico", 6.0, "copa", self.ingredientes[1], self.ingredientes[3], self.ingredientes[5]),
        ]

    @patch('controllers.heladeria_controler.Producto.query.all')
    def test_listar_productos(self, mock_query_all):
        # Simular productos
        mock_query_all.return_value = self.productos
        productos = HeladeriaController.listar_productos()
        self.assertEqual(len(productos), 10)
        self.assertEqual(productos[0].nombre, "Helado de Vainilla")

    @patch('controllers.heladeria_controler.Ingrediente.query.all')
    def test_listar_ingredientes(self, mock_query_all):
        # Simular ingredientes
        mock_query_all.return_value = list(self.ingredientes.values())
        ingredientes = HeladeriaController.listar_ingredientes()
        self.assertEqual(len(ingredientes), 9)
        self.assertEqual(ingredientes[0].nombre, "Leche")

    @patch('controllers.heladeria_controler.Producto.query.filter_by')
    def test_vender_producto_exitoso(self, mock_filter_by):
        # Simular el producto
        mock_filter_by.return_value.first.return_value = self.productos[0]

        mensaje = HeladeriaController.vender_producto("Helado de Vainilla")
        self.assertEqual(mensaje, "¡Vendido!")
        self.assertEqual(self.ingredientes[1].inventario, 49)  # Leche
        self.assertEqual(self.ingredientes[3].inventario, 99)  # Azúcar
        self.assertEqual(self.ingredientes[5].inventario, 9)   # Vainilla

    @patch('controllers.heladeria_controler.Producto.query.filter_by')
    def test_vender_producto_falla(self, mock_filter_by):
        # Simular el producto
        mock_filter_by.return_value.first.return_value = self.productos[0]

        # Reducir inventario para provocar fallo
        self.ingredientes[5].inventario = 0  # Vainilla agotada

        with self.assertRaises(ValueError) as context:
            HeladeriaController.vender_producto("Helado de Vainilla")
        self.assertEqual(str(context.exception), "¡Oh no! Nos hemos quedado sin Vainilla.")

    def test_calcular_costo_producto(self):
        # Verificar cálculo del costo del primer producto
        costo = self.productos[0].calcular_costo()
        self.assertEqual(costo, 1.5 + 0.8 + 5.0)

    def test_calcular_calorias_producto(self):
        # Verificar cálculo de calorías del primer producto
        calorias = self.productos[0].calcular_calorias()
        self.assertEqual(calorias, 42 + 400 + 20)

    @patch('controllers.heladeria_controler.Producto.query.all')
    def test_producto_mas_rentable(self, mock_query_all):
        # Simular productos
        mock_query_all.return_value = self.productos
        productos = HeladeriaController.listar_productos()

        # Encontrar producto más rentable
        mas_rentable = max(productos, key=lambda p: p.rentabilidad())
        self.assertEqual(mas_rentable.nombre, "Torta Helada")  # Producto con mayor precio público

    def test_rentabilidad_producto(self):
        # Verificar rentabilidad de un producto
        rentabilidad = self.productos[0].rentabilidad()
        self.assertEqual(rentabilidad, 10.0 - (1.5 + 0.8 + 5.0))

if __name__ == '__main__':
    unittest.main()
