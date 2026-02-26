import pandas as pd
import os
from datetime import datetime

# Nombres de los archivos Excel
ARCHIVO_STOCK = 'stock_kiosco.xlsx'
ARCHIVO_VENTAS = 'ventas_kiosco.xlsx'

def inicializar_archivos():
    """Crea los archivos Excel con sus cabeceras si no existen."""
    if not os.path.exists(ARCHIVO_STOCK):
        columnas = ['Codigo', 'Producto', 'Categoria', 'Precio_Costo', 'Precio_Venta', 'Stock_Actual']
        pd.DataFrame(columns=columnas).to_excel(ARCHIVO_STOCK, index=False)
        print(f"✔️ Creado: {ARCHIVO_STOCK}")
    
    if not os.path.exists(ARCHIVO_VENTAS):
        columnas = ['Fecha', 'Producto', 'Cantidad', 'Total_Venta', 'Ganancia_Neta']
        pd.DataFrame(columns=columnas).to_excel(ARCHIVO_VENTAS, index=False)
        print(f"✔️ Creado: {ARCHIVO_VENTAS}")

def agregar_producto(codigo, nombre, categoria, costo, venta, stock):
    """Guarda o actualiza un producto en el inventario."""
    df = pd.read_excel(ARCHIVO_STOCK)
    
    nuevo_prod = {
        'Codigo': str(codigo),
        'Producto': nombre,
        'Categoria': categoria,
        'Precio_Costo': float(costo),
        'Precio_Venta': float(venta),
        'Stock_Actual': int(stock)
    }
    
    # Si el producto ya existe (por código), lo eliminamos para sobreescribirlo
    df = df[df['Codigo'].astype(str) != str(codigo)]
    
    df = pd.concat([df, pd.DataFrame([nuevo_prod])], ignore_index=True)
    df.to_excel(ARCHIVO_STOCK, index=False)
    print(f"💾 {nombre} guardado en el inventario.")

def registrar_venta_db(items_carrito):
    """Resta 1 unidad de stock y guarda la ganancia en el historial de ventas."""
    df_stock = pd.read_excel(ARCHIVO_STOCK)
    df_ventas = pd.read_excel(ARCHIVO_VENTAS)
    
    registros_nuevos = []
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in items_carrito:
        nombre_prod = item['nombre']
        precio_v = item['precio']
        
        # 1. Buscar el producto en el stock para obtener el costo y restar stock
        try:
            idx = df_stock.index[df_stock['Producto'] == nombre_prod].tolist()[0]
            
            # Restamos una unidad del stock
            df_stock.at[idx, 'Stock_Actual'] -= 1
            
            # Calculamos ganancia neta
            costo = df_stock.at[idx, 'Precio_Costo']
            ganancia = precio_v - costo
            
            # Guardamos el registro de esta unidad vendida
            registros_nuevos.append({
                'Fecha': fecha_actual,
                'Producto': nombre_prod,
                'Cantidad': 1,
                'Total_Venta': precio_v,
                'Ganancia_Neta': ganancia
            })
        except Exception as e:
            print(f"Error al procesar {nombre_prod}: {e}")

    # Guardar cambios definitivos en los Excel
    df_stock.to_excel(ARCHIVO_STOCK, index=False)
    df_ventas = pd.concat([df_ventas, pd.DataFrame(registros_nuevos)], ignore_index=True)
    df_ventas.to_excel(ARCHIVO_VENTAS, index=False)
    print("📈 Ventas y stock actualizados prolijamente.")