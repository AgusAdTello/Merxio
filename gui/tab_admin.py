import customtkinter as ctk
from tkinter import messagebox
from database import obtener_resumen_ganancias, actualizar_precios_masivo, obtener_faltantes

class TabAdmin:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.parent, text="📊 Dashboard de Negocio", font=("Arial", 22, "bold")).pack(pady=15)
        
        self.lbl_ventas = ctk.CTkLabel(self.parent, text="Ventas Hoy: $0.00", font=("Arial", 18))
        self.lbl_ventas.pack()
        
        self.lbl_ganancia = ctk.CTkLabel(self.parent, text="Ganancia Neta: $0.00", font=("Arial", 18), text_color="#2ecc71")
        self.lbl_ganancia.pack(pady=5)

        # Módulo Inflación
        ctk.CTkLabel(self.parent, text="📈 Ajuste por Inflación (%)", font=("Arial", 16, "bold")).pack(pady=(20,5))
        self.ent_inf = ctk.CTkEntry(self.parent, placeholder_text="Ej: 10")
        self.ent_inf.pack()
        ctk.CTkButton(self.parent, text="Aplicar Aumento", fg_color="#e67e22", command=self.ejecutar_aumento).pack(pady=10)

        # Faltantes
        ctk.CTkLabel(self.parent, text="⚠️ Alertas de Reposición", font=("Arial", 16, "bold")).pack(pady=10)
        self.txt_faltantes = ctk.CTkTextbox(self.parent, width=500, height=120)
        self.txt_faltantes.pack()
        
        self.actualizar_datos()

    def ejecutar_aumento(self):
        try:
            porc = float(self.ent_inf.get())
            if messagebox.askyesno("Confirmar", f"¿Aumentar todos los precios un {porc}%?"):
                actualizar_precios_masivo(porc)
                messagebox.showinfo("Éxito", "Precios actualizados.")
        except:
            messagebox.showerror("Error", "Ingresa un porcentaje válido.")

    def actualizar_datos(self):
        v, g = obtener_resumen_ganancias()
        self.lbl_ventas.configure(text=f"Ventas Hoy: ${v:,.2f}")
        self.lbl_ganancia.configure(text=f"Ganancia Neta: ${g:,.2f}")
        
        faltantes = obtener_faltantes()
        self.txt_faltantes.delete("1.0", "end")
        for f in faltantes:
            self.txt_faltantes.insert("end", f"Falta: {f[0]} (Quedan: {f[1]})\n")