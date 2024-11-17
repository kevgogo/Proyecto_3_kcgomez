class Heladeria:
    def __init__(self):
        self.ingredientes = []  # Lista de ingredientes disponibles
        self.productos = []     # Lista de productos disponibles

    def agregar_ingrediente(self, ingrediente):
        self.ingredientes.append(ingrediente)

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def listar_ingredientes(self):
        return self.ingredientes

    def listar_productos(self):
        return self.productos

    def buscar_ingrediente_por_nombre(self, nombre):
        for ingrediente in self.ingredientes:
            if ingrediente.nombre.lower() == nombre.lower():
                return ingrediente
        return None

    def buscar_producto_por_nombre(self, nombre):
        for producto in self.productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None