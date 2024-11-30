import os
import shutil

def limpiar_caché(base_dir=None, exclude_dirs=None):
    """Limpia archivos y carpetas de caché en el proyecto, excluyendo directorios específicos."""
    base_dir = base_dir or os.getcwd()
    exclude_dirs = exclude_dirs or [".venv"]

    print("Iniciando limpieza de caché...")
    for root, dirs, files in os.walk(base_dir, topdown=False):
        # Ignorar directorios excluidos
        if any(root.startswith(os.path.join(base_dir, exclude)) for exclude in exclude_dirs):
            continue

        # Eliminar carpetas de caché
        for dir_name in dirs:
            if dir_name == "__pycache__" or dir_name in [".pytest_cache", ".mypy_cache"]:
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Eliminada carpeta: {dir_path}")
                except Exception as e:
                    print(f"No se pudo eliminar {dir_path}: {e}")

        # Eliminar archivos de caché
        for file_name in files:
            if file_name.endswith(".pyc") or file_name.endswith(".pyo"):
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"Eliminado archivo: {file_path}")
                except Exception as e:
                    print(f"No se pudo eliminar {file_path}: {e}")
    print("Limpieza de caché completada.")

if __name__ == "__main__":
    limpiar_caché()
