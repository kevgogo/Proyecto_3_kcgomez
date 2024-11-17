from app.extensions import db

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=False)

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

    def es_sano(self):
        return self.calorias < 300

    def renovar_inventario(self, cantidad):
        self.inventario += cantidad
        self._guardar_cambios()
