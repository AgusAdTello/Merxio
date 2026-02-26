import customtkinter as ctk
import pandas as pd
from datetime import datetime
from database import inicializar_archivos, agregar_producto, registrar_venta_db, ARCHIVO_STOCK

# Configuración visual moderna
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppKiosco(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kiosco Pro v1.0 - Gestión Offline")
        self.geometry("900x650")
        
        # Al arrancar, verificamos que existan los Excel
        inicializar_archivos()

        # Variables de estado del carrito
        self.carrito = [] # Aquí guardaremos {'nombre': ..., 'precio': ...}
        self.total_actual = 0.0

        # --- Creación de Pestañas ---
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(padx=20, pady=20, fill="both", expand=True)
        self.tab_ventas = self.tabs.add("Caja / Ventas")
        self.tab_stock = self.tabs.add("Inventario / Carga")

        self.setup_ventas()
        self.setup_stock()

    # --- DISEÑO: PESTAÑA DE VENTAS ---
    def setup_ventas(self):
        self.lbl_titulo_v = ctk.CTkLabel(self.tab_ventas, text="🛒 Terminal de Cobro", font=("Arial", 24, "bold"))
        self.lbl_titulo_v.pack(pady=10)

        # Buscador por nombre
        self.ent_buscar = ctk.CTkEntry(self.tab_ventas, placeholder_text="Escribí el nombre del producto...", width=400)
        self.ent_buscar.pack(pady=10)
        
        btn_add = ctk.CTkButton(self.tab_ventas, text="+ Agregar al Carrito", command=self.agregar_item)
        btn_add.pack(pady=5)

        # Visualización del carrito (Ticket)
        self.txt_carrito = ctk.CTkTextbox(self.tab_ventas, width=550, height=250, font=("Courier New", 14))
        self.txt_carrito.pack(pady=10)

        # Total y Botón de Cobro
        self.lbl_total = ctk.CTkLabel(self.tab_ventas, text="TOTAL: $0.00", font=("Arial", 36, "bold"), text_color="#2ecc71")
        self.lbl_total.pack(pady=10)

        btn_cobrar = ctk.CTkButton(self.tab_ventas, text="CONCRETAR VENTA (COBRAR)", 
                                   fg_color="#27ae60", hover_color="#1e8449", 
                                   height=50, font=("Arial", 16, "bold"),
                                   command=self.procesar_cobro)
        btn_cobrar.pack(pady=10)

    # --- DISEÑO: PESTAÑA DE STOCK ---
    def setup_stock(self):
        ctk.CTkLabel(self.tab_stock, text="📦 Carga de Inventario", font=("Arial", 20, "bold")).pack(pady=10)

        # Campos de entrada
        self.e_cod = ctk.CTkEntry(self.tab_stock, placeholder_text="Código de Barras", width=300)
        self.e_nom = ctk.CTkEntry(self.tab_stock, placeholder_text="Nombre del Producto (Ej: Coca Cola 500ml)", width=300)
        self.e_costo = ctk.CTkEntry(self.tab_stock, placeholder_text="Precio Costo Proveedor ($)", width=300)
        self.e_venta = ctk.CTkEntry(self.tab_stock, placeholder_text="Precio Venta Público ($)", width=300)
        self.e_stock = ctk.CTkEntry(self.tab_stock, placeholder_text="Stock Inicial (Unidades)", width=300)

        for e in [self.e_cod, self.e_nom, self.e_costo, self.e_venta, self.e_stock]:
            e.pack(pady=5)

        btn_save = ctk.CTkButton(self.tab_stock, text="Guardar en Inventario", 
                                 fg_color="#2980b9", command=self.guardar_stock_ui)
        btn_save.pack(pady=20)

    # --- LÓGICA DE FUNCIONAMIENTO ---
    def agregar_item(self):
        busqueda = self.ent_buscar.get().lower()
        if not busqueda: return

        try:
            df = pd.read_excel(ARCHIVO_STOCK)
            # Buscamos si el texto ingresado está en la columna Producto
            resultado = df[df['Producto'].str.lower().str.contains(busqueda, na=False)]
            
            if not resultado.empty:
                prod = resultado.iloc[0]
                nombre = prod['Producto']
                precio = prod['Precio_Venta']
                
                # GUARDAMOS EL DICCIONARIO PARA DATABASE.PY
                self.carrito.append({"nombre": nombre, "precio": precio})
                
                self.total_actual += precio
                
                # Actualizar pantalla
                self.txt_carrito.insert("end", f"{nombre.ljust(30)} ${precio:>8.2f}\n")
                self.lbl_total.configure(text=f"TOTAL: ${self.total_actual:.2f}")
                self.ent_buscar.delete(0, 'end')
            else:
                print("Producto no encontrado.")
        except Exception as e:
            print(f"Error al buscar: {e}")

    def procesar_cobro(self):
        if not self.carrito:
            print("El carrito está vacío.")
            return

        # 1. Llamamos a la función de database.py que resta stock y guarda ganancias
        registrar_venta_db(self.carrito)
        
        # 2. Limpiamos todo para la próxima venta
        self.carrito = []
        self.total_actual = 0.0
        self.txt_carrito.delete("1.0", "end")
        self.lbl_total.configure(text="TOTAL: $0.00")
        print("Venta finalizada y registrada en Excel.")

    def guardar_stock_ui(self):
        try:
            # Capturamos datos y validamos que los números sean correctos
            cod = self.e_cod.get()
            nom = self.e_nom.get()
            costo = float(self.e_costo.get())
            venta = float(self.e_venta.get())
            stock = int(self.e_stock.get())

            agregar_producto(cod, nom, "Gral", costo, venta, stock)
            
            # Limpiar campos después de guardar
            for e in [self.e_cod, self.e_nom, self.e_costo, self.e_venta, self.e_stock]:
                e.delete(0, 'end')
            print(f"Éxito: {nom} cargado correctamente.")
        except ValueError:
            print("Error: Los precios y el stock deben ser números.")

if __name__ == "__main__":
    app = AppKiosco()
    app.mainloop()