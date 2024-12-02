import csv
import os
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

from models.producto import Producto
from models.ingrediente import Base, Complemento, Ingrediente
from models.usuario import Usuario
from config import Config

def inicializar_base_de_datos():
    
    from sqlalchemy import create_engine, text, inspect

    """
    Inicializa la base de datos: crea tablas y carga datos iniciales desde CSV.
    """
    try:
        connection = db.engine.connect()
        Config.conditional_print("Database connection successful.")
        connection.close()
    except Exception as e:
        Config.conditional_print(f"Database connection failed: {e}")

    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if not tables:
            Config.conditional_print("No tables found. Ready to create tables.")
            db.create_all()
            Config.conditional_print("Tables created successfully.")
        else:
            with db.engine.connect() as conn:
                sqlite_sequence_exists = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';")).fetchone()

            Config.conditional_print(f"Tables found ({tables}). Proceeding to truncate...")
            with db.engine.begin() as conn:
                for table in tables:
                    conn.execute(text(f"DELETE FROM {table}"))
                    if sqlite_sequence_exists:
                        conn.execute(text(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table}'"))
            Config.conditional_print("All tables truncated successfully.")

        # Cargar datos
        cargar_datos()
    except Exception as e:
        Config.conditional_print(f"Error with inspector or database operations: {e}")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def cargar_datos():
    """
    Carga datos desde archivos CSV en la base de datos.
    """
    cargar_ingredientes(os.path.join(BASE_DIR, "ingredientes.csv"))
    cargar_productos(os.path.join(BASE_DIR, "productos.csv"))
    cargar_productos_ingredientes(os.path.join(BASE_DIR, "productos_por_ingredientes.csv"))
    cargar_usuarios(os.path.join(BASE_DIR, "usuarios.csv"))

def cargar_ingredientes(file_path):
    """
    Carga los ingredientes desde un archivo CSV a la base de datos.
    El archivo debe incluir una columna 'tipo' para diferenciar entre 'base', 'complemento' y 'generico'.

    Args:
        file_path (str): Ruta del archivo CSV.
    """
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tipo = row.get('tipo', 'generico').lower()

            try:
                # Crear instancias según el tipo
                if tipo == 'base':
                    ingrediente = Base(
                        nombre=row['nombre'],
                        precio=float(row['precio']),
                        calorias=int(row['calorias']),
                        inventario=int(row['inventario']),
                        es_vegetariano=row['es_vegetariano'].lower() == 'true',
                        sabor=row['sabor'] 
                    )
                elif tipo == 'complemento':
                    ingrediente = Complemento(
                        nombre=row['nombre'],
                        precio=float(row['precio']),
                        calorias=int(row['calorias']),
                        inventario=int(row['inventario']),
                        es_vegetariano=row['es_vegetariano'].lower() == 'true'
                    )
                else:  # Tipo generico o ingrediente estándar
                    ingrediente = Ingrediente(
                        nombre=row['nombre'],
                        precio=float(row['precio']),
                        calorias=int(row['calorias']),
                        inventario=int(row['inventario']),
                        es_vegetariano=row['es_vegetariano'].lower() == 'true'
                    )

                # Guardar en la base de datos
                db.session.add(ingrediente)

            except KeyError as e:
                Config.conditional_print(f"Error en los datos: Faltan columnas requeridas {e}")
            except ValueError as e:
                Config.conditional_print(f"Error en el formato de los datos: {e}")

        # Confirmar los cambios
        db.session.commit()
        Config.conditional_print("Ingredientes cargados exitosamente.")

def cargar_productos(ruta_csv):
    """
    Carga los datos de productos desde un archivo CSV.
    """
    try:
        with open(ruta_csv, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                producto = Producto(
                    nombre=fila["nombre"],
                    precio_publico=float(fila["precio_publico"]),
                    tipo=fila["tipo"]
                )
                db.session.merge(producto)  # Merge para evitar duplicados
        db.session.commit()
        Config.conditional_print("Datos de productos cargados correctamente.")
    except Exception as e:
        Config.conditional_print(f"Error al cargar datos de productos: {e}")

def cargar_productos_ingredientes(ruta_csv):
    """
    Carga las relaciones entre productos e ingredientes desde un archivo CSV.
    """
    try:
        with open(ruta_csv, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                producto_id = int(fila["producto_id"])
                ingrediente_id = int(fila["ingrediente_id"])

                # Buscar producto e ingrediente
                producto = Producto.query.get(producto_id)
                ingrediente = Ingrediente.query.get(ingrediente_id)

                if not producto:
                    Config.conditional_print(f"Producto con ID {producto_id} no encontrado. Saltando.")
                    continue

                if not ingrediente:
                    Config.conditional_print(f"Ingrediente con ID {ingrediente_id} no encontrado. Saltando.")
                    continue

                # Verificar si la relación ya existe
                if ingrediente not in producto.ingredientes:
                    producto.ingredientes.append(ingrediente)

        db.session.commit()
        Config.conditional_print("Relaciones productos-ingredientes cargadas correctamente.")
    except Exception as e:
        Config.conditional_print(f"Error al cargar relaciones productos-ingredientes: {e}")

def cargar_usuarios(ruta_csv):
    """
    Carga los datos de usuarios desde un archivo CSV.
    """
    try:
        with open(ruta_csv, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                usuario = Usuario(
                    username=fila["username"],
                    password=fila["password"],
                    es_admin=fila["es_admin"].lower() == 'true',
                    es_empleado=fila["es_empleado"].lower() == 'true'
                )
                db.session.merge(usuario)  # Merge para evitar duplicados
        db.session.commit()
        Config.conditional_print("Datos de usuarios cargados correctamente.")
    except Exception as e:
        Config.conditional_print(f"Error al cargar datos de usuarios: {e}")
