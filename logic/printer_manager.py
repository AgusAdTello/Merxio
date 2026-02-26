import os
from datetime import datetime

def generar_ticket_texto(items, total):
    """Crea un archivo de texto con el formato de un ticket legal/comercial."""
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"tickets/ticket_{fecha_str}.txt"
    
    # Crear carpeta de tickets si no existe
    if not os.path.exists('tickets'):
        os.makedirs('tickets')
        
    linea = "-" * 40
    contenido = [
        "*** MERXIO - COMPROBANTE DE VENTA ***",
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        linea,
        f"{'Producto'.ljust(25)} {'Precio'.rjust(12)}",
        linea
    ]
    
    for item in items:
        contenido.append(f"{item['nombre'][:25].ljust(25)} ${item['precio']:>11.2f}")
        
    contenido.append(linea)
    contenido.append(f"{'TOTAL:'.ljust(25)} ${total:>11.2f}")
    contenido.append(linea)
    contenido.append("\nGracias por su compra!")
    
    with open(nombre_archivo, "w") as f:
        f.write("\n".join(contenido))
    
    # Abrir el archivo automáticamente para que el usuario pueda imprimir (Windows)
    os.startfile(nombre_archivo)