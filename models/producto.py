from app.extensions import db
from models.producto_ingrediente import productos_por_ingredientes  # Importa la tabla intermedia

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    ingredientes = db.relationship(
        'Ingrediente',
        secondary=productos_por_ingredientes,
        back_populates='productos'
    )

    def __init__(self, nombre, precio_publico, tipo):
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.tipo = tipo

    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.ingredientes)

    def calcular_calorias(self):
        return sum(ingrediente.calorias for ingrediente in self.ingredientes)

    def rentabilidad(self):
        return self.precio_publico - self.calcular_costo()
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio_publico": self.precio_publico,
            "tipo": self.tipo,
            "ingredientes": [ingrediente.to_dict() for ingrediente in self.ingredientes]  # IDs de ingredientes relacionados
        }

    def __repr__(self):
        return f"<Producto(nombre={self.nombre}, precio_publico={self.precio_publico}, tipo={self.tipo})>"