from app.extensions import db

productos_por_ingredientes = db.Table(
    'productos_por_ingredientes',
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
)
