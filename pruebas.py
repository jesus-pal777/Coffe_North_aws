import datetime as dt
from main import CargaDatos
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


CargaDatos = CargaDatos()


# Carga de archivo CSV

     # Echange rate
df_Exchange_rate = CargaDatos.Cargar_CSV("exchange_rates.csv")
df_Exchange_rate = CargaDatos.CambioFecha(df_Exchange_rate, 'fecha')
df_Exchange_rate = CargaDatos.TextoLimpio(df_Exchange_rate, 'currency')




    # sales
df_Sales = CargaDatos.Cargar_CSV("sales.csv")
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'venta_id')
df_Sales = CargaDatos.CambioFecha(df_Sales, 'fecha_hora')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'tienda_id')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'sku')
df_Sales = CargaDatos.CambioEnteros(df_Sales, 'cantidad')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'moneda')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'tipo_comprobante')







# Carga de archivo JSON

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






# -------------------------- complementos en los difetnes DataFrames -------------------------- #


    # Denbido a que se tiene en el DF_SKU el campo sku_erp con alguno valores nulos y en el DF Cost_History también se tiene el campo sku_erp, 
    # se puede realizar una unión para obtener la información del df Cost_History y llenar el campo costo en el DF_SKU.


# Paso 1 
# Creamos una lista de todos los sku_erp extraidos del Df Cost_History para posteriormente realizar una unión con el DF_SKU
erps_unicos = df_Cost_History['sku_erp'].unique()


# Paso 2
# Se crea un diccionario con la llave que será la división de los sku_erp (los digitos) y valor que sera el sku completo
# los skus son de la siguiente forma ERP-PROV-MX-002-B como el divisor se puso que era el guión (-) se toma el 3 valor empezando desde el 0
# obtenemos el valor 002 el cual es el la llave y el valor es todo el sku obtenido.
diccionario_sku = {}
for sku in erps_unicos:
    clave = sku.split('-')[3]
    diccionario_sku[clave]=sku


# Paso 3
# Sacamos los valores a comparar de nuestro df SKU para que se haga la comparación con la llave del diccionario previamente creado. El cual se logra
# con el -3 que extrae de la cadena de texto de esa columna los 3 último caracteres se tiene el formato CN-00002 el cual extraería el 002
claves_extraidas = df_SKU['sku_pos'].str[-3:]


# Paso 4
# Haremos el llenado sobre la columna faltante con los datos previamente obtenidos. El cual hace lo siguiente 
df_SKU['sku_erp']= df_SKU['sku_erp'].fillna(claves_extraidas.map(diccionario_sku))




    # Llenamos la siguiente columna ya que en handle se tiene valores None; se observa que es la combinación de la columna nombre del df Cost History 
    # unido con un - y con la diferencia de los últimos 3 digitos que los distinguen del sku por lo que primero se hará una distinción de los valores
    # None para no realizar un proceso computacional extra sobre todas el df    



    # Paso 1 creamos una lista única con los valores del sku de los valores que se tienen nulo en la columna handle y solo tendremos el sku de dichos
    # valores

handle_faltante = df_SKU[df_SKU['handle'].isna()]['sku_erp'].unique()


    # Paso 2 
    # Sobre el df de Cost_history haremos el match del sku que previamente obtivos de los valores nulos y eliminando los duplicados
    # esto por si es que se tiene el mismo sku muchas veces. Y Posterior haremos la limpieza de estos nombre todo con minusculas y la unión
    # con el caracter - 

df_nombre_filtrado = df_Cost_History[df_Cost_History['sku_erp'].isin(handle_faltante)].drop_duplicates(subset=['sku_erp']).copy()
df_nombre_filtrado['nombre_limpio'] =(
    df_nombre_filtrado['nombre']
    .str.lower()
    .str.replace(' ','-')
)



    # Paso 3
    # Agregaremos una columna nueva así como se agregó el 'nombre limpio' pero ahora sobre pero ahora con los últimos 3 dígitos para posterior
    # unirlos con el nombre columna nombre_limpio que previamente se colocaron en minusculas y se quitó el espacio y se colocó un guión '-'

df_nombre_filtrado['digitos_finales'] = df_nombre_filtrado['sku_erp'].str.split('-').str[3]
df_nombre_filtrado['handle_generado'] = df_nombre_filtrado['nombre_limpio']+'-'+df_nombre_filtrado['digitos_finales']


    # Paso 4
    # Generemoa un diccionario con la información ya generada

diccionario_handle = df_nombre_filtrado.set_index('sku_erp')['handle_generado'].to_dict()



    # Paso 5
    # Rellenamos la columna con el handle ya generado, esto para que tengamos y con la función .map 

df_SKU['handle'] = df_SKU['handle'].fillna(df_SKU['sku_erp'].map(diccionario_handle))




    # Debido a que se tienen RFC sin llenar lo que se hace es que se coloca en valores nulos el rfc generico proporcionado por MX

    # Se hace la limpieza de la columna y solo los valores de la fila que sea nulos, null, None se cambian por el rfc generico XAXX010101000
df_Ecommerce['customer_rfc']= df_Ecommerce['customer_rfc'].fillna('XAXX010101000')



# ------------------ Guardar archivos limpios -------------------


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



# ------------ Pruebas ----------- #

print("\n \n \n \n \n \n \n \n"+70*"+")
print(f"Sección de pruebas")
print(70*"+"+ "\n \n \n \n \n \n \n \n")


# ----------------------------- CSV ------------------------------- #

print(20*"+")
print(f"Sección de pruebas de carga de archivo CSV")
print(20*"+"+ "\n \n \n \n \n \n \n \n")

# --------- Xchange Rate Limpio  -------- #
print(5*"+")
print(f"CSV || Xchange Rate")
print(5*"+")
print(f"{df_Exchange_rate.head(5)} \n \n \n \n \n \n \n \n")
print(f"{df_Exchange_rate.tail(5)} \n \n \n \n \n \n \n \n")



# --------- Sales Limpio -------- #
print(5*"+")
print(f"CSV || Sales")
print(5*"+")
print(f"{df_Sales.head(5)} \n \n \n \n \n \n \n \n")
print(f"{df_Sales.tail(5)} \n \n \n \n \n \n \n \n")


# ----------------------------- JSON ------------------------------- #
print(20*"+")
print(f"Sección de pruebas de carga de archivo JSON")
print(20*"+"+ "\n \n \n")


# --------- Tiendas Limpio -------- #
print(5*"+")
print(f"JSON || Tiendas")
print(5*"+" )
print(f"{df_Tiendas.head(5)} \n \n \n \n \n \n \n \n")
print(f"{df_Tiendas.tail(5)} \n \n \n \n \n \n \n \n")

# --------- SKU Limpio -------- #
print(5*"+")
print(f"JSON || SKU")
print(5*"+")
print(f"{df_SKU.head(5)} \n \n \n \n \n \n \n \n")
print(f"{df_SKU.tail(5)} \n \n \n \n \n \n \n \n")


# ---------- Cost History -------- #
print(5*"+")
print(f"JSON || Cost History")
print(5*"+") 
print(f"{df_Cost_History.head(5)} \n \n \n \n \n \n \n \n ")
print(f"{df_Cost_History.tail(5)} \n \n \n \n \n \n \n \n ")


# ----------------------------- Parquet ------------------------------- #
print(20*"+")
print(f"Sección de pruebas de carga de archivo Parquet")
print(20*"+")
print(f"{df_Ecommerce.head(5)} \n \n \n \n")
print(f"{df_Ecommerce.tail(5)} \n \n")
#print(f"{df_Ecommerce.columns.to_list()} \n \n")
#print(f"{df_Ecommerce.info()} \n \n")