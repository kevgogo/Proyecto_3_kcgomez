from app.extensions import db

class HeladeriaController:

    @staticmethod
    def manejar_errores(func):
        """
        Decorador para manejar errores en los métodos del controlador.
        Incluye el nombre del método en los mensajes.
        """
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return {
                    "message": f"{func.__name__.replace('_', ' ').capitalize()} completado con éxito.",
                    "result": result
                }, 200
            except ValueError as e:
                return {
                    "error": f"Error en {func.__name__.replace('_', ' ')}: {str(e)}"
                }, 400
            except Exception as e:
                return {
                    "error": f"Error inesperado en {func.__name__.replace('_', ' ')}: {str(e)}"
                }, 500
        return wrapper
    
    # ------------------- Métodos para Productos -------------------

    @staticmethod
    @manejar_errores
    def listar_productos():
        from models.producto import Producto
        productos = Producto.query.all()
        return [producto.serialize() for producto in productos]

    @staticmethod
    @manejar_errores
    def obtener_producto_por_id(id):
        from models.producto import Producto
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        return producto.serialize()

    @staticmethod
    @manejar_errores
    def buscar_producto_por_nombre(nombre):
        from models.producto import Producto
        producto = Producto.query.filter_by(nombre=nombre).first()
        if not producto:
            raise ValueError(f"Producto con nombre '{nombre}' no encontrado.")
        return producto.serialize()

    @staticmethod
    @manejar_errores
    def obtener_calorias_producto(id):
        from models.producto import Producto
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        return {"calorias": producto.calorias}

    @staticmethod
    @manejar_errores
    def obtener_rentabilidad_producto(id):
        from models.producto import Producto
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        return {"rentabilidad": producto.rentabilidad}

    @staticmethod
    @manejar_errores
    def obtener_costo_producto(id):
        from models.producto import Producto
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        return {"costo": producto.costo}

    @staticmethod
    @manejar_errores
    def vender_producto_por_id(id):
        from models.producto import Producto
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        
        for ingrediente in producto.ingredientes:
            if ingrediente.inventario <= 0:
                raise ValueError(f"No hay suficiente inventario para {ingrediente.nombre}.")
        
        for ingrediente in producto.ingredientes:
            ingrediente.reducir_inventario(1)

        db.session.commit()
        return f"Producto '{producto.nombre}' vendido exitosamente."

    @staticmethod
    @manejar_errores
    def reabastecer_producto(id, cantidad):
        from models.producto import Producto
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        
        if cantidad <= 0:
            raise ValueError("La cantidad para reabastecer debe ser mayor a cero.")

        for ingrediente in producto.ingredientes:
            ingrediente.abastecer(cantidad)

        db.session.commit()
        return f"Producto con ID {id} reabastecido con {cantidad} unidades por ingrediente."

    @staticmethod
    @manejar_errores
    def renovar_inventario_producto(id, cantidad):
        from models.producto import Producto
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado.")
        
        if cantidad <= 0:
            raise ValueError("La cantidad para renovar debe ser mayor a cero.")

        for ingrediente in producto.ingredientes:
            ingrediente.renovar_inventario(cantidad)

        db.session.commit()
        return f"Inventario del producto con ID {id} renovado a {cantidad} unidades por ingrediente."

    # ------------------- Métodos para Ingredientes -------------------

    @staticmethod
    @manejar_errores
    def listar_ingredientes():
        from models.ingrediente import Ingrediente
        ingredientes = Ingrediente.query.all()
        return [ingrediente.serialize() for ingrediente in ingredientes]

    @staticmethod
    @manejar_errores
    def obtener_ingrediente_por_id(id):
        from models.ingrediente import Ingrediente
        ingrediente = Ingrediente.query.get(id)
        if not ingrediente:
            raise ValueError(f"Ingrediente con ID {id} no encontrado.")
        return ingrediente.serialize()

    @staticmethod
    @manejar_errores
    def buscar_ingrediente_por_nombre(nombre):
        from models.ingrediente import Ingrediente
        ingrediente = Ingrediente.query.filter_by(nombre=nombre).first()
        if not ingrediente:
            raise ValueError(f"Ingrediente con nombre '{nombre}' no encontrado.")
        return ingrediente.serialize()

    @staticmethod
    @manejar_errores
    def es_ingrediente_sano(id):
        from models.ingrediente import Ingrediente
        ingrediente = Ingrediente.query.get(id)
        if not ingrediente:
            raise ValueError(f"Ingrediente con ID {id} no encontrado.")
        return {"es_sano": ingrediente.es_sano()}
