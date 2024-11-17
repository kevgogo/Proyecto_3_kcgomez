from app.extensions import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    ingrediente1_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    ingrediente2_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    ingrediente3_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)

    ingrediente1 = db.relationship('Ingrediente', foreign_keys=[ingrediente1_id])
    ingrediente2 = db.relationship('Ingrediente', foreign_keys=[ingrediente2_id])
    ingrediente3 = db.relationship('Ingrediente', foreign_keys=[ingrediente3_id])

    def __init__(self, nombre, precio_publico, tipo, ingrediente1, ingrediente2, ingrediente3):
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.tipo = tipo
        self.ingrediente1 = ingrediente1
        self.ingrediente2 = ingrediente2
        self.ingrediente3 = ingrediente3

    def calcular_costo(self):
        return self.ingrediente1.precio + self.ingrediente2.precio + self.ingrediente3.precio

    def calcular_calorias(self):
        return self.ingrediente1.calorias + self.ingrediente2.calorias + self.ingrediente3.calorias

    def rentabilidad(self):
        return self.precio_publico - self.calcular_costo()
