from app.extensions import db

class HeladeriaController:
    @staticmethod
    def listar_ingredientes():
        from models.ingrediente import Ingrediente
        return Ingrediente.query.all()

    @staticmethod
    def listar_productos():
        from models.producto import Producto
        return Producto.query.all()

    @staticmethod
    def buscar_ingrediente_por_nombre(nombre):
        from models.ingrediente import Ingrediente
        return Ingrediente.query.filter_by(nombre=nombre).first()

    @staticmethod
    def buscar_producto_por_nombre(nombre):
        from models.producto import Producto
        return Producto.query.filter_by(nombre=nombre).first()

    @staticmethod
    def vender_producto(nombre_producto):
        from models.producto import Producto
        producto = Producto.query.filter_by(nombre=nombre_producto).first()
        if not producto:
            raise ValueError(f"Producto '{nombre_producto}' no encontrado.")
        
        ingredientes = [producto.ingrediente1, producto.ingrediente2, producto.ingrediente3]
        for ingrediente in ingredientes:
            if ingrediente.inventario <= 0:
                raise ValueError(f"¡Oh no! Nos hemos quedado sin {ingrediente.nombre}.")

        for ingrediente in ingredientes:
            ingrediente.reducir_inventario(1)

        db.session.commit()
        return "¡Vendido!"
