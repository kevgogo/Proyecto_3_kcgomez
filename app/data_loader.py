import csv
import os
from config import Config
from app.utils import conditional_print
from app.extensions import db

def cargar_datos():
    from models.ingrediente import Ingrediente
    from models.producto import Producto
    base_dir = os.path.abspath(os.path.dirname(__file__))

    archivos_csv = {
        'ingredientes': {
            'path': os.path.join(base_dir, '../data/ingredientes.csv'),
            'campos': lambda row: Ingrediente(
                nombre=row['nombre'],
                precio=float(row['precio']),
                calorias=int(row['calorias']),
                inventario=int(row['inventario']),
                es_vegetariano=row['es_vegetariano'].strip().lower() in ['true', '1', 'yes']
            )
        },
        'productos': {
            'path': os.path.join(base_dir, '../data/productos.csv'),
            'campos': lambda row: Producto(
                nombre=row['nombre'],
                precio_publico=float(row['precio_publico']),
                tipo=row['tipo'],
                ingrediente1=Ingrediente.query.get(int(row['ingrediente1_id'])),
                ingrediente2=Ingrediente.query.get(int(row['ingrediente2_id'])),
                ingrediente3=Ingrediente.query.get(int(row['ingrediente3_id']))
            )
        },
    }

    for tipo, datos in archivos_csv.items():
        csv_path = datos['path']
        campos = datos['campos']

        conditional_print(f"Cargando datos de {tipo} desde {csv_path}...")
        if not os.path.exists(csv_path):
            conditional_print(f"Archivo {csv_path} no encontrado. Saltando.")
            continue

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    registro = campos(row)
                    db.session.add(registro)
            conditional_print(f"Datos de {tipo} cargados exitosamente.")
        except Exception as e:
            conditional_print(f"Error al cargar datos de {tipo}: {e}")

    db.session.commit()
    conditional_print("Todos los datos se cargaron exitosamente.")