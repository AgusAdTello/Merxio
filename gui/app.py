import customtkinter as ctk
from database import inicializar_archivos
from gui.tab_ventas import TabVentas
from gui.tab_stock import TabStock
from gui.tab_admin import TabAdmin

class AppMerxio(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Merxio Pro - Sistema de Gestión")
        self.geometry("1000x750")
        
        # 1. Asegurar que los archivos Excel existan antes de cargar la UI
        inicializar_archivos()

        # 2. Configuración del contenedor de pestañas
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(padx=20, pady=20, fill="both", expand=True)
        
        # 3. Creación de las pestañas físicas
        tab_v = self.tabs.add("Caja / Ventas")
        tab_s = self.tabs.add("Inventario / Carga")
        tab_a = self.tabs.add("Administración")

        # 4. Inyección de las clases de interfaz en cada pestaña
        # Pasamos 'self' si alguna pestaña necesitara comunicarse con otra en el futuro
        self.ui_ventas = TabVentas(tab_v)
        self.ui_stock = TabStock(tab_s)
        self.ui_admin = TabAdmin(tab_a)

        # 5. Opcional: Vincular eventos globales
        # Por ejemplo, actualizar el dashboard de admin cada vez que se cambia a esa pestaña
        self.tabs.configure(command=self.al_cambiar_pestana)

    def al_cambiar_pestana(self):
        """Actualiza los datos de administración cuando el usuario entra a esa pestaña."""
        if self.tabs.get() == "Administración":
            self.ui_admin.actualizar_datos()

if __name__ == "__main__":
    # Esto permite probar la clase app.py de forma independiente si fuera necesario
    app = AppMerxio()
    app.mainloop()