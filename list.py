import os

def listar_estructura(carpeta_base, excluir=[".venv", "__pycache__", ".git", ".vscode"], nivel=0):
    for elemento in os.listdir(carpeta_base):
        ruta = os.path.join(carpeta_base, elemento)
        
        # Comprobar si el elemento es una carpeta o archivo excluido
        if os.path.basename(ruta) in excluir:
            continue

        # Imprimir la estructura
        print(" " * nivel * 2 + f"|-- {elemento}")

        # Si es un directorio, recorrerlo recursivamente
        if os.path.isdir(ruta):
            listar_estructura(ruta, excluir, nivel + 1)

# Cambia "ruta_del_proyecto" por la ruta base de tu proyecto
ruta_del_proyecto = "K:/Development/CURSOS/UNIANDES/Modulo 2/Proyecto_2_kc.gomez"
listar_estructura(ruta_del_proyecto)
