from app.extensions import db, bcrypt

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    es_empleado = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, es_admin=False, es_empleado=False):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.es_admin = es_admin
        self.es_empleado = es_empleado

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
