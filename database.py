import pandas as pd
import os
from datetime import datetime

# Nombres de los archivos Excel (Base de Datos)
ARCHIVO_STOCK = 'stock_kiosco.xlsx'
ARCHIVO_VENTAS = 'ventas_kiosco.xlsx'

def inicializar_archivos():
    """Crea los archivos Excel con sus cabeceras si no existen."""
    if not os.path.exists(ARCHIVO_STOCK):
        columnas = ['Codigo', 'Producto', 'Categoria', 'Precio_Costo', 'Precio_Venta', 'Stock_Actual']
        pd.DataFrame(columns=columnas).to_excel(ARCHIVO_STOCK, index=False)
    
    if not os.path.exists(ARCHIVO_VENTAS):
        columnas = ['Fecha', 'Producto', 'Cantidad', 'Total_Venta', 'Ganancia_Neta']
        pd.DataFrame(columns=columnas).to_excel(ARCHIVO_VENTAS, index=False)

def agregar_producto(codigo, nombre, categoria, costo, venta, stock):
    """Guarda un producto nuevo o actualiza uno existente usando el código como ID."""
    df = pd.read_excel(ARCHIVO_STOCK)
    nuevo_prod = {
        'Codigo': str(codigo),
        'Producto': nombre,
        'Categoria': categoria,
        'Precio_Costo': float(costo),
        'Precio_Venta': float(venta),
        'Stock_Actual': int(stock)
    }
    # Si el código ya existe, eliminamos la fila vieja para actualizar
    df = df[df['Codigo'].astype(str) != str(codigo)]
    df = pd.concat([df, pd.DataFrame([nuevo_prod])], ignore_index=True)
    df.to_excel(ARCHIVO_STOCK, index=False)

def registrar_venta_db(items_carrito):
    """Procesa el carrito: descuenta stock y registra ventas con ganancia neta."""
    df_stock = pd.read_excel(ARCHIVO_STOCK)
    df_ventas = pd.read_excel(ARCHIVO_VENTAS)
    registros_nuevos = []
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in items_carrito:
        nombre_prod = item['nombre']
        precio_v = item['precio']
        try:
            idx = df_stock.index[df_stock['Producto'] == nombre_prod].tolist()[0]
            df_stock.at[idx, 'Stock_Actual'] -= 1
            costo = df_stock.at[idx, 'Precio_Costo']
            ganancia = precio_v - costo
            registros_nuevos.append({
                'Fecha': fecha_actual,
                'Producto': nombre_prod,
                'Cantidad': 1,
                'Total_Venta': precio_v,
                'Ganancia_Neta': ganancia
            })
        except Exception as e:
            print(f"Error procesando {nombre_prod}: {e}")

    df_stock.to_excel(ARCHIVO_STOCK, index=False)
    df_ventas = pd.concat([df_ventas, pd.DataFrame(registros_nuevos)], ignore_index=True)
    df_ventas.to_excel(ARCHIVO_VENTAS, index=False)

def obtener_resumen_ganancias():
    """Calcula las ventas y ganancias del día actual."""
    if not os.path.exists(ARCHIVO_VENTAS): return 0.0, 0.0
    df = pd.read_excel(ARCHIVO_VENTAS)
    if df.empty: return 0.0, 0.0
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    hoy = datetime.now().date()
    ventas_hoy = df[df['Fecha'].dt.date == hoy]
    total_v = ventas_hoy['Total_Venta'].sum()
    total_g = ventas_hoy['Ganancia_Neta'].sum()
    return total_v, total_g

def actualizar_precios_masivo(porcentaje):
    """Aumenta todos los precios de venta por un porcentaje (inflación)."""
    df = pd.read_excel(ARCHIVO_STOCK)
    factor = 1 + (porcentaje / 100)
    df['Precio_Venta'] *= factor
    df.to_excel(ARCHIVO_STOCK, index=False)

def obtener_faltantes(limite=5):
    """Retorna productos con stock bajo."""
    df = pd.read_excel(ARCHIVO_STOCK)
    faltantes = df[df['Stock_Actual'] <= limite]
    return faltantes[['Producto', 'Stock_Actual']].values.tolist()