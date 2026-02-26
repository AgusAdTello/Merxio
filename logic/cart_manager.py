class CartManager:
    def __init__(self):
        self.items = []
        self.total = 0.0

    def agregar_producto(self, nombre, precio):
        self.items.append({"nombre": nombre, "precio": precio})
        self.total += precio

    def limpiar(self):
        self.items = []
        self.total = 0.0

    def obtener_resumen(self):
        return self.items, self.total