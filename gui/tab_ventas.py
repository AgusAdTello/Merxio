import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
from database import registrar_venta_db, ARCHIVO_STOCK
from logic.cart_manager import CartManager
from logic.printer_manager import generar_ticket_texto

class TabVentas:
    def __init__(self, parent):
        self.parent = parent
        
        # Instanciamos la lógica separada del carrito
        self.cart = CartManager()
        
        # Variable para el buscador en tiempo real
        self.sv_buscar = ctk.StringVar()
        self.sv_buscar.trace_add("write", self.buscar_tiempo_real)
        
        self.setup_ui()

    def setup_ui(self):
        # Título
        ctk.CTkLabel(self.parent, text="🛒 Terminal de Ventas", font=("Arial", 24, "bold")).pack(pady=10)
        
        # Buscador
        self.ent_buscar = ctk.CTkEntry(
            self.parent, 
            textvariable=self.sv_buscar,
            placeholder_text="Escribí el nombre del producto...", 
            width=450
        )
        self.ent_buscar.pack(pady=10)
        
        # Etiqueta de sugerencia dinámica
        self.lbl_sugerencia = ctk.CTkLabel(self.parent, text="Coincidencia: Ninguna", text_color="gray")
        self.lbl_sugerencia.pack()

        # Botón para agregar (también funciona con la tecla Enter si haces el bind en AppMerxio)
        ctk.CTkButton(
            self.parent, 
            text="+ AGREGAR AL CARRITO", 
            fg_color="#34495e", 
            command=self.agregar_item
        ).pack(pady=10)

        # Visualización de Ticket
        self.txt_carrito = ctk.CTkTextbox(self.parent, width=650, height=250, font=("Courier New", 14))
        self.txt_carrito.pack(pady=10)

        # Total
        self.lbl_total = ctk.CTkLabel(self.parent, text="TOTAL: $0.00", font=("Arial", 36, "bold"), text_color="#2ecc71")
        self.lbl_total.pack(pady=10)

        # Botón Cobrar e Imprimir
        self.btn_cobrar = ctk.CTkButton(
            self.parent, 
            text="COBRAR E IMPRIMIR TICKET", 
            fg_color="#27ae60", 
            hover_color="#1e8449",
            height=50, 
            font=("Arial", 18, "bold"),
            command=self.procesar_cobro
        )
        self.btn_cobrar.pack(pady=10)

    def buscar_tiempo_real(self, *args):
        busqueda = self.sv_buscar.get().lower()
        if len(busqueda) < 2:
            self.lbl_sugerencia.configure(text="Coincidencia: Ninguna", text_color="gray")
            return

        try:
            df = pd.read_excel(ARCHIVO_STOCK)
            res = df[df['Producto'].str.lower().str.contains(busqueda, na=False)]
            if not res.empty:
                match = res.iloc[0]['Producto']
                self.lbl_sugerencia.configure(text=f"Coincidencia: {match}", text_color="#3498db")
            else:
                self.lbl_sugerencia.configure(text="No encontrado", text_color="#e74c3c")
        except: pass

    def agregar_item(self):
        busqueda = self.sv_buscar.get().lower()
        try:
            df = pd.read_excel(ARCHIVO_STOCK)
            res = df[df['Producto'].str.lower().str.contains(busqueda, na=False)]
            
            if not res.empty:
                prod = res.iloc[0]
                nombre = prod['Producto']
                precio = prod['Precio_Venta']
                
                # Usamos la clase CartManager
                self.cart.agregar_producto(nombre, precio)
                
                # Actualizar pantalla
                _, total = self.cart.obtener_resumen()
                self.txt_carrito.insert("end", f"{nombre[:30].ljust(30)} ${precio:>8.2f}\n")
                self.lbl_total.configure(text=f"TOTAL: ${total:.2f}")
                
                # Limpiar buscador
                self.sv_buscar.set("")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró: '{busqueda}'")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al buscar producto: {e}")

    def procesar_cobro(self):
        items, total = self.cart.obtener_resumen()
        
        if not items:
            messagebox.showwarning("Atención", "El carrito está vacío.")
            return

        try:
            # 1. Registrar en la base de datos (descontar stock y guardar ganancias)
            registrar_venta_db(items)
            
            # 2. Generar el archivo de ticket y abrirlo
            generar_ticket_texto(items, total)
            
            # 3. Limpiar todo
            self.cart.limpiar()
            self.txt_carrito.delete("1.0", "end")
            self.lbl_total.configure(text="TOTAL: $0.00")
            
            messagebox.showinfo("Venta Exitosa", "La venta ha sido registrada e impresa.")
            
        except Exception as e:
            messagebox.showerror("Error al cobrar", f"Ocurrió un problema: {e}")