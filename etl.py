from main import CargaDatos
import pandas as pd


CargaDatos = CargaDatos()

    # Exchange rate
df_Exchange_rate = CargaDatos.Cargar_CSV("exchange_rates.csv")
df_Exchange_rate = CargaDatos.CambioFecha(df_Exchange_rate, 'fecha')
df_Exchange_rate = CargaDatos.TextoLimpio(df_Exchange_rate, 'currency')

    # Sales
df_Sales = CargaDatos.Cargar_CSV("sales.csv")
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'venta_id')
df_Sales = CargaDatos.CambioFecha(df_Sales, 'fecha_hora')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'tienda_id')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'sku')
df_Sales = CargaDatos.CambioEnteros(df_Sales, 'cantidad')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'moneda')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'tipo_comprobante')



    # JSON

df_Inventory = CargaDatos.Cargar_Json("inventory.json")


    # Tiendas
df_Tiendas  = df_Inventory['dfTiendas']
df_Tiendas = CargaDatos.TextoLimpio(df_Tiendas, 'tienda_id')
df_Tiendas = CargaDatos.TextoLimpio(df_Tiendas, 'ciudad')
df_Tiendas = CargaDatos.TextoLimpio(df_Tiendas, 'region')
df_Tiendas = CargaDatos.TextoLimpio(df_Tiendas, 'timezone')



    # SKU 
df_SKU = df_Inventory['dfSKU']
df_SKU = CargaDatos.TextoLimpio(df_SKU, 'sku_pos')
df_SKU = CargaDatos.TextoLimpio(df_SKU, 'sku_erp')
df_SKU = CargaDatos.TextoLimpio(df_SKU, 'handle')

    # Archivo con diccionario anidados
df_Catalogo = df_Inventory['dfCatalogo']
    # Primer aplandado del JSON
df_Catalogo_ = CargaDatos.AplanarJson(df_Catalogo, 'productos')
    # Segundo aplandado del JSON
df_Cost_History = CargaDatos.SegundoAplanadoJson(df_Catalogo_, 'cost_history')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'sku_erp')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'nombre')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'categoria')
df_Cost_History = CargaDatos.CambioFecha(df_Cost_History, 'fecha_vigencia')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'proveedor')



# Carga de archivo parquet
df_Ecommerce = CargaDatos.Cargar_Parquet("ecommerce_orders.parquet")
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'order_id')
df_Ecommerce = CargaDatos.CambioFecha(df_Ecommerce, 'fecha')
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'product_handle')
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'currency')
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'customer_name')
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'customer_email')
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'customer_rfc')
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'shipping_city')
df_Ecommerce = CargaDatos.TextoLimpio(df_Ecommerce, 'shipping_address')


    # Limpieza extra y llenado de columnas con valores nulos

erps_unicos = df_Cost_History['sku_erp'].unique()

diccionario_sku = {}
for sku in erps_unicos:
    clave = sku.split('-')[3]
    diccionario_sku[clave]=sku

claves_extraidas = df_SKU['sku_pos'].str[-3:]

df_SKU['sku_erp']= df_SKU['sku_erp'].fillna(claves_extraidas.map(diccionario_sku))


handle_faltante = df_SKU[df_SKU['handle'].isna()]['sku_erp'].unique()

df_nombre_filtrado = df_Cost_History[df_Cost_History['sku_erp'].isin(handle_faltante)].drop_duplicates(subset=['sku_erp']).copy()
df_nombre_filtrado['nombre_limpio'] =(
    df_nombre_filtrado['nombre']
    .str.lower()
    .str.replace(' ','-')
)

df_nombre_filtrado['digitos_finales'] = df_nombre_filtrado['sku_erp'].str.split('-').str[3]
df_nombre_filtrado['handle_generado'] = df_nombre_filtrado['nombre_limpio']+'-'+df_nombre_filtrado['digitos_finales']

diccionario_handle = df_nombre_filtrado.set_index('sku_erp')['handle_generado'].to_dict()

df_SKU['handle'] = df_SKU['handle'].fillna(df_SKU['sku_erp'].map(diccionario_handle))



df_Ecommerce['customer_rfc']= df_Ecommerce['customer_rfc'].fillna('XAXX010101000')


print(f"Carga de archivos limpios en formato parquet")
try:
    df_Exchange_rate.to_parquet('Archivos/Exchange_Rate.parquet', index= False)
    df_Sales.to_parquet('Archivos/Sales.parquet', index = False)
    df_Tiendas.to_parquet('Archivos/tiendas.parquet', index = False)
    df_SKU.to_parquet('Archivos/sku.parquet', index=False)
    df_Cost_History.to_parquet('Archivos/Cost_history.parquet', index = False)
    df_Ecommerce.to_parquet("Archivos/Ecommerce.parquet", index = False)
    print("Archivos cargados con exito, sobre carpeta /Archivos/")
except Exception as e:
    print(f"Error al cargar los archivos {e}")