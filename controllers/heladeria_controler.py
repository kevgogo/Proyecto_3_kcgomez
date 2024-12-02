from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from models.producto import Producto
from models.ingrediente import Ingrediente
from models.usuario import Usuario
from app.utils import manejar_errores

class HeladeriaController:
    @staticmethod
    @manejar_errores
    def listar_productos():
        """
        Lista todos los productos disponibles.
        """
        productos = Producto.query.all()
        return {
            "message": "Lista de productos obtenida exitosamente.",
            "result": [producto.to_dict() for producto in productos]
        }, 200

    @staticmethod
    @manejar_errores
    def obtener_producto_por_id(id):
        """
        Obtiene un producto por su ID.
        """
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        return {
            "message": "Producto encontrado.",
            "result": producto.to_dict()
        }, 200

    @staticmethod
    @manejar_errores
    def buscar_producto_por_nombre(nombre):
        """
        Busca un producto por su nombre.
        """
        productos = Producto.query.filter(Producto.nombre.ilike(f"%{nombre}%")).all()
        return {
            "message": "Búsqueda de productos completada.",
            "result": [producto.to_dict() for producto in productos]
        }, 200

    @staticmethod
    @manejar_errores
    def obtener_calorias_producto(id):
        """
        Obtiene las calorías totales de un producto, calculadas a partir de sus ingredientes.
        """
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        calorias_totales = sum(ingrediente.calorias for ingrediente in producto.ingredientes)
        return {
            "message": f"Calorías totales del producto '{producto.nombre}' calculadas.",
            "result": {"producto_id": id, "calorias": calorias_totales}
        }, 200

    @staticmethod
    @manejar_errores
    def obtener_rentabilidad_producto(id):
        """
        Calcula la rentabilidad de un producto.
        """
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        return {
            "message": f"Rentabilidad del producto '{producto.nombre}' obtenida.",
            "result": {"producto_id": id, "rentabilidad": producto.rentabilidad}
        }, 200

    @staticmethod
    @manejar_errores
    def obtener_costo_producto(id):
        """
        Obtiene el costo de producción de un producto.
        """
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        return {
            "message": f"Costo de producción del producto '{producto.nombre}' obtenido.",
            "result": {"producto_id": id, "costo": producto.costo}
        }, 200

    @staticmethod
    @manejar_errores
    def vender_producto_por_id(id):
        """
        Procesa la venta de un producto y ajusta el inventario de sus ingredientes.
        """
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        
        try:
            producto.vender()
            return {
                "message": f"Producto '{producto.nombre}' vendido exitosamente.",
                "result": {"producto_id": id}
            }, 200
        except ValueError as e:
            return {
                "message": str(e),
                "result": {"producto_id": id}
            }, 400

    @staticmethod
    @manejar_errores
    def reabastecer_producto(id, cantidad):
        """
        Reabastece los ingredientes de un producto.
        """
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")

        if cantidad <= 0:
            raise ValueError("La cantidad para reabastecer debe ser mayor a cero.")

        resultado = []
        for ingrediente in producto.ingredientes:
            cantidad_anterior = ingrediente.cantidad
            ingrediente.abastecer(cantidad)
            resultado.append({
                "ingrediente_id": ingrediente.id,
                "ingrediente_nombre": ingrediente.nombre,
                "cantidad_anterior": cantidad_anterior,
                "cantidad_actual": ingrediente.cantidad
            })

        db.session.commit()
        return {
            "message": f"Producto '{producto.nombre}' reabastecido.",
            "result": resultado
        }, 200

    @staticmethod
    @manejar_errores
    def renovar_inventario_producto(id, cantidad):
        """
        Renueva el inventario de los ingredientes de un producto.
        """
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")

        if cantidad <= 0:
            raise ValueError("La cantidad para renovar debe ser mayor a cero.")

        resultado = []
        for ingrediente in producto.ingredientes:
            cantidad_anterior = ingrediente.cantidad
            ingrediente.renovar_inventario(cantidad)
            resultado.append({
                "ingrediente_id": ingrediente.id,
                "ingrediente_nombre": ingrediente.nombre,
                "cantidad_anterior": cantidad_anterior,
                "cantidad_actual": ingrediente.cantidad
            })

        db.session.commit()
        return {
            "message": f"Inventario del producto '{producto.nombre}' renovado.",
            "result": resultado
        }, 200

    @staticmethod
    @manejar_errores
    def listar_ingredientes():
        """
        Lista todos los ingredientes disponibles.
        """
        ingredientes = Ingrediente.query.all()
        return {
            "message": "Lista de ingredientes obtenida exitosamente.",
            "result": [ingrediente.to_dict() for ingrediente in ingredientes]
        }, 200

    @staticmethod
    @manejar_errores
    def obtener_ingrediente_por_id(id):
        """
        Obtiene un ingrediente por su ID.
        """
        ingrediente = Ingrediente.query.get(id)
        if not ingrediente:
            raise ValueError(f"Ingrediente con ID {id} no encontrado.")
        return {
            "message": "Ingrediente encontrado.",
            "result": ingrediente.to_dict()
        }, 200

    @staticmethod
    @manejar_errores
    def buscar_ingrediente_por_nombre(nombre):
        """
        Busca un ingrediente por su nombre.
        """
        ingredientes = Ingrediente.query.filter(Ingrediente.nombre.ilike(f"%{nombre}%")).all()
        return {
            "message": "Búsqueda de ingredientes completada.",
            "result": [ingrediente.to_dict() for ingrediente in ingredientes]
        }, 200

    @staticmethod
    @manejar_errores
    def es_ingrediente_sano(id):
        """
        Verifica si un ingrediente es considerado sano.
        """
        ingrediente = Ingrediente.query.get(id)
        if not ingrediente:
            raise ValueError(f"Ingrediente con ID {id} no encontrado.")
        return {
            "message": f"Ingrediente '{ingrediente.nombre}' es {'sano' if ingrediente.es_sano else 'no sano'}.",
            "result": {"ingrediente_id": id, "es_sano": ingrediente.es_sano}
        }, 200

    @staticmethod
    @manejar_errores
    def obtener_estadisticas_generales():
        """
        Devuelve estadísticas generales para el dashboard.
        """
        total_productos = Producto.query.count()
        total_ingredientes = Ingrediente.query.count()
        total_usuarios = Usuario.query.count()

        productos_mas_vendidos = Producto.query.filter(Producto.ventas > 0).order_by(Producto.ventas.desc()).all()
        total_ventas = 0

        productos_mas_vendidos_data = []
        for producto in productos_mas_vendidos:
            valor_total_producto = producto.ventas * producto.precio_publico
            total_ventas += valor_total_producto
            productos_mas_vendidos_data.append({
                "id": producto.id,
                "nombre": producto.nombre,
                "ventas": producto.ventas,
                "precio_publico": producto.precio_publico,
                "valor_total": valor_total_producto
            })

        return {
            "message": "Estadísticas generales obtenidas con éxito.",
            "result": {
                "total_productos": total_productos,
                "total_ingredientes": total_ingredientes,
                "total_usuarios": total_usuarios,
                "total_ventas": total_ventas,
                "productos_mas_vendidos": productos_mas_vendidos_data
            }
        }, 200
