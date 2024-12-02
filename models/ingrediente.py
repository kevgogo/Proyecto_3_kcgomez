from app.extensions import db
from models.producto_ingrediente import productos_por_ingredientes  # Importa la tabla intermedia

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=False)

    productos = db.relationship(
        'Producto',
        secondary=productos_por_ingredientes,
        back_populates='ingredientes'
    )

    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano):
        self.nombre = nombre
        self.precio = precio
        self.calorias = calorias
        self.inventario = inventario
        self.es_vegetariano = es_vegetariano

    def _guardar_cambios(self):
        if hasattr(db, 'session'):
            db.session.commit()

    def abastecer(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.inventario += cantidad
        self._guardar_cambios()

    def reducir_inventario(self, cantidad):
        if self.inventario >= cantidad:
            self.inventario -= cantidad
            self._guardar_cambios()
        else:
            raise ValueError(f"No hay suficiente inventario para {self.nombre}.")
        
    def renovar_inventario(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.inventario = cantidad
        self._guardar_cambios()

    def es_sano(self):
        return self.calorias is not None and self.calorias < 300

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'calorias': self.calorias,
            'inventario': self.inventario,
            'es_vegetariano': self.es_vegetariano,
            'es_sano': self.es_sano(),
        }
    
    def __repr__(self):
        return f"<Ingrediente(nombre={self.nombre}, precio={self.precio}, calorias={self.calorias})>"