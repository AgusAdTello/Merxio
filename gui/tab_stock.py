import customtkinter as ctk
from tkinter import messagebox
from database import agregar_producto

class TabStock:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.parent, text="📦 Carga de Inventario", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.e_cod = ctk.CTkEntry(self.parent, placeholder_text="Código de Barras", width=300)
        self.e_nom = ctk.CTkEntry(self.parent, placeholder_text="Nombre del Producto", width=300)
        self.e_costo = ctk.CTkEntry(self.parent, placeholder_text="Costo ($)", width=300)
        self.e_venta = ctk.CTkEntry(self.parent, placeholder_text="Venta ($)", width=300)
        self.e_stock = ctk.CTkEntry(self.parent, placeholder_text="Stock inicial", width=300)

        for e in [self.e_cod, self.e_nom, self.e_costo, self.e_venta, self.e_stock]:
            e.pack(pady=5)
            
        ctk.CTkButton(self.parent, text="Guardar Producto", fg_color="#2980b9", 
                      command=self.guardar_datos).pack(pady=20)

    def guardar_datos(self):
        try:
            costo = float(self.e_costo.get().replace(',', '.'))
            venta = float(self.e_venta.get().replace(',', '.'))
            stock = int(self.e_stock.get())
            
            agregar_producto(self.e_cod.get(), self.e_nom.get(), "Gral", costo, venta, stock)
            messagebox.showinfo("Éxito", f"Producto {self.e_nom.get()} guardado.")
            for e in [self.e_cod, self.e_nom, self.e_costo, self.e_venta, self.e_stock]: 
                e.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Revisa que los precios y el stock sean números.")