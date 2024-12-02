from app.extensions import db
from models.producto_ingrediente import productos_por_ingredientes  # Importa la tabla intermedia

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    ventas = db.Column(db.Integer, default=0)  # Ventas registradas para el producto
    
    ingredientes = db.relationship(
        'Ingrediente',
        secondary=productos_por_ingredientes,
        back_populates='productos'
    )

    def __init__(self, nombre, precio_publico, tipo):
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.tipo = tipo

    def _guardar_cambios(self):
        if hasattr(db, 'session'):
            db.session.commit()

    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.ingredientes)

    def calcular_calorias(self):
        return sum(ingrediente.calorias for ingrediente in self.ingredientes)

    def rentabilidad(self):
        return self.precio_publico - self.calcular_costo()
    
    def tiene_stock_suficiente(self):
        """
        Verifica si el producto tiene stock suficiente basado en el inventario de sus ingredientes.
        """
        for ingrediente in self.ingredientes:
            if ingrediente.inventario <= 0:
                return False
        return True
        
    def vender(self):
        """
        Procesa la venta del producto, reduciendo el inventario de sus ingredientes.
        Lanza una excepción si no hay inventario suficiente.
        """
        # Usar tiene_stock_suficiente para validar
        if not self.tiene_stock_suficiente():
            raise ValueError(f"No hay suficiente inventario para el producto '{self.nombre}'.")

        # Reducir el inventario de los ingredientes
        for ingrediente in self.ingredientes:
            ingrediente.inventario -= 1  # Reduce 1 por venta (ajusta según las necesidades)

        # Incrementar el contador de ventas del producto
        self.ventas += 1
        self._guardar_cambios()
        
    def total_vendido(self):
        """
        Procesa la cantidad vendida del producto
        """
        return self.ventas * self.precio_publico

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio_publico": self.precio_publico,
            "calorias": self.calcular_calorias(),
            "costo": self.calcular_costo(),
            "rentabilidad": self.rentabilidad(),
            "tipo": self.tipo,
            "stock_suficiente": self.tiene_stock_suficiente(),
            "ingredientes": [ingrediente.to_dict() for ingrediente in self.ingredientes]  # IDs de ingredientes relacionados
        }

    def __repr__(self):
        return f"<Producto(nombre={self.nombre}, precio_publico={self.precio_publico}, tipo={self.tipo})>"