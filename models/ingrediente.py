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
    tipo = db.Column(db.String(20), default="generico")  # "base", "complemento", "generico"

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'generico'
    }

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

    # Métodos comunes
    def _guardar_cambios(self):
        if hasattr(db, 'session'):
            db.session.commit()

    def abastecer(self, cantidad):
        """
        Incrementa el inventario del complemento por una cantidad específica.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.inventario += cantidad
        self._guardar_cambios()

    def reducir_inventario(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        if self.inventario >= cantidad:
            self.inventario -= cantidad
            self._guardar_cambios()
        else:
            raise ValueError(f"No hay suficiente inventario para {self.nombre}.")

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
            'tipo': self.tipo,
        }

    def __repr__(self):
        return f"<Ingrediente(nombre={self.nombre}, precio={self.precio}, calorias={self.calorias})>"

class Base(Ingrediente):
    __mapper_args__ = {
        'polymorphic_identity': 'base',  # Identidad específica para polimorfismo
    }

    sabor = db.Column(db.String(50), nullable=True)  # Campo adicional para Base

    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano, sabor):
        super().__init__(nombre, precio, calorias, inventario, es_vegetariano)
        self.sabor = sabor
        self.tipo = "base"  # Configura el tipo como 'base'
        
    def abastecer(self, cantidad):
        """
        Incrementa el inventario de la base por una cantidad específica.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.inventario += cantidad
        self._guardar_cambios()

    def renovar_inventario(self, cantidad):
        """
        Renueva el inventario del complemento, reiniciándolo al valor proporcionado.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.inventario = cantidad
        self._guardar_cambios()

    def to_dict(self):
        """
        Convierte el objeto Base a un diccionario serializable.
        Incluye el campo adicional 'sabor'.
        """
        data = super().to_dict()
        data['sabor'] = self.sabor
        return data

    def __repr__(self):
        """
        Representación en texto para depuración.
        """
        return f"<Base(nombre={self.nombre}, precio={self.precio}, calorias={self.calorias}, sabor={self.sabor})>"

class Complemento(Ingrediente):
    __mapper_args__ = {
        'polymorphic_identity': 'complemento',  # Identidad específica para polimorfismo
    }

    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano):
        super().__init__(nombre, precio, calorias, inventario, es_vegetariano)
        self.tipo = "complemento"  # Configura el tipo como 'complemento'

    def abastecer(self, cantidad):
        """
        Incrementa el inventario de la base por una cantidad específica.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.inventario += cantidad
        self._guardar_cambios()

    def renovar_inventario(self, cantidad):
        """
        Renueva el inventario del complemento, reiniciándolo al valor proporcionado.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.inventario = cantidad
        self._guardar_cambios()

    def __repr__(self):
        """
        Representación en texto para depuración.
        """
        return f"<Complemento(nombre={self.nombre}, precio={self.precio}, calorias={self.calorias})>"
