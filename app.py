
from app import app

def limpiar_proyecto():
  import os
  import shutil
  for root, dirs, files in os.walk(os.getcwd()):
      for dir_name in dirs:
          if dir_name == "__pycache__":
              shutil.rmtree(os.path.join(root, dir_name))
      for file_name in files:
          if file_name.endswith(".pyc") or file_name.endswith(".pyo"):
              os.remove(os.path.join(root, file_name))


if __name__ == '__main__':
  limpiar_proyecto()
  app.run(debug=True)
