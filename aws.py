import pandas as pd
import s3fs
import json


class CargaDatos:

    def __init__(self):
        pass

    # Método para realizar la carga de archivo csv
    def Cargar_CSV(self, ArchivoCSV):
        try:
            if ArchivoCSV.startswith("s3://"):
                fs = s3fs.S3FileSystem()
                with fs.open(ArchivoCSV, 'rb') as f:
                    df = pd.read_csv(f)
            else:
                df = pd.read_csv(ArchivoCSV)
            print(f"Se realizó la carga de datos correctamente desde el archivo CSV: {ArchivoCSV}")
            return df
        except Exception as e:
            print(f"CRITICAL: Error al cargar el CSV {ArchivoCSV} debido a: {e}")
            return None

    # Método para realizar la carja de archivo JSON y aplanarlo
    def Cargar_Json(self, ArchivoJson):
        try:
            if ArchivoJson.startswith("s3://"):
                fs = s3fs.S3FileSystem()
                with fs.open(ArchivoJson, 'r', encoding='utf-8') as j:
                    datosCrudos = json.load(j)
            else:
                with open(ArchivoJson, 'r', encoding='utf-8') as j:
                    datosCrudos = json.load(j)

            TablasJson = {
                "dfTiendas": pd.DataFrame(datosCrudos['tiendas_info']),
                "dfSKU": pd.DataFrame(datosCrudos['sku_mappings']),
                "dfCatalogo": pd.DataFrame(datosCrudos['catalogo']),
                "dfCorte": pd.DataFrame(datosCrudos['snapshots'])
            }
            print(f"Se realizó la carga de datos correctamente desde el archivo JSON: {ArchivoJson}")
            return TablasJson
        except Exception as e:
            print(f"CRITICAL: Error al cargar el JSON {ArchivoJson} debido a: {e}")
            return None

    # Primer aplanado del JSON
    def AplanarJson(self, dfJson, NombreColumna):
        try:
            dfJsonLimpio = pd.json_normalize(dfJson[NombreColumna])
            return dfJsonLimpio
        except Exception as e:
            print(f'Se tuvo un problema al realizar el aplanado del JSON: {e}')
            return None
        
    # En caso de que se requiera un segundo aplanado del JSON, se puede utilizar el siguiente método
    def SegundoAplanadoJson(self, df, columna):
        try:
           df_Exploratorio = df.explode(columna).reset_index(drop=True)
           df_ExploratorioColumnas =  df_Exploratorio[columna].apply(lambda x: x if isinstance(x, dict) else {}).tolist()
           df_Aplanado = pd.json_normalize(df_ExploratorioColumnas)
           df_AplanadoLimpio = pd.concat([df_Exploratorio.drop(columns = [columna]),df_Aplanado], axis =1)
           return df_AplanadoLimpio
        except Exception as e:
            print(f'Se tuvo un problema al realizar el segundo aplanado del JSON: {e}')
            return None  

    # Método para realizar la carga de archivo parquet
    def Cargar_Parquet(self, ArchivoParquet):
        try:
            if ArchivoParquet.startswith("s3://"):
                fs = s3fs.S3FileSystem()
                with fs.open(ArchivoParquet, 'rb') as f:
                    df = pd.read_parquet(f)
            else:
                df = pd.read_parquet(ArchivoParquet)
            print(f"Se realizó la carga de datos correctamente desde el archivo Parquet: {ArchivoParquet}")
            return df
        except Exception as e:
            print(f"CRITICAL: Error al cargar el Parquet {ArchivoParquet} debido a: {e}")
            return None

    # Método para limpieza de columnas de texto
    def TextoLimpio(self, df, columna):
        
        # Se hace una doble validación ya que al momento de correr el scirpt se tuvo error como objeto nulo
        if df is not None and columna in df.columns:
            try:
                if df[columna].dtype == 'object':
                    df[columna] = df[columna].str.strip()
                else:
                    print(f"La columna {columna} no es de tipo texto")                    
            except Exception as e:
                print(f"Se tuvo un problema al limpiar la columna {columna}: {e}")
        else:
            print(f"La columna {columna} no existe o el DataFrame es None")
        return df

    # Método para cambiar el tipo de dato a entero
    def CambioEnteros(self, df, columna):
        
        # Se hace una doble validación ya que al momento de correr el scirpt se tuvo error como objeto nulo
        if df is not None and columna in df.columns:
            try:
                if df[columna].dtype != 'Int64':
                    df[columna] = pd.to_numeric(df[columna], errors='coerce').astype('Int64')
                else:
                    print(f"La columna {columna} ya es de tipo entero")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a entero: {e}")
        else:
            print(f"La columna {columna} no existe o el DataFrame es None")
        return df

    # Método para cambiar el tipo de dato a flotante
    def CambioFlotantes(self, df, columna):
        if df is not None and columna in df.columns:
            try:
                if df[columna].dtype != 'float64':
                    df[columna] = pd.to_numeric(df[columna], errors='coerce').astype('float64')
                else:
                    print(f"La columna {columna} ya es de tipo flotante")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a flotante: {e}")
        else:
            print(f"La columna {columna} no existe o el DataFrame es None")
        return df

    # Metodo para cambiar el tipo de dato a fecha
    def CambioFecha(self, df, columna):
        
        # Se hace una doble validación ya que al momento de correr el scirpt se tuvo error como objeto nulo
        if df is not None and columna in df.columns:
            try:
                if not pd.api.types.is_datetime64_any_dtype(df[columna]):
                    df[columna] = pd.to_datetime(df[columna], errors='coerce')
                else:
                    print(f"La columna {columna} ya es de tipo fecha")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a fecha: {e}")
        else:
            print(f"La columna {columna} no existe o el DataFrame es None")
        return df


    # Metodo para cambiar el tipo de dato a string
    def CambioString(self, df, columna):
        # Se hace una doble validación ya que al momento de correr el scirpt se tuvo error como objeto nulo
        if df is not None and columna in df.columns:
            try:
                if df[columna].dtype != 'object':
                    df[columna] = df[columna].astype(str)
                else:
                    print(f"La columna {columna} ya es de tipo string")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a string: {e}")
        else:
            print(f"La columna {columna} no existe o el DataFrame es None")
        return df


CargaDatos = CargaDatos()

ruta_crudo = "s3://amz-coffenorth-data/crudo/"
ruta_limpio = "s3://amz-coffenorth-data/limpio/"

# Carga de Exchange rate
df_Exchange_rate = CargaDatos.Cargar_CSV(ruta_crudo + "exchange_rates.csv")
df_Exchange_rate = CargaDatos.CambioFecha(df_Exchange_rate, 'fecha')
df_Exchange_rate = CargaDatos.TextoLimpio(df_Exchange_rate, 'currency')

# Carga de Sales
df_Sales = CargaDatos.Cargar_CSV(ruta_crudo + "sales.csv")
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'venta_id')
df_Sales = CargaDatos.CambioFecha(df_Sales, 'fecha_hora')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'tienda_id')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'sku')
df_Sales = CargaDatos.CambioEnteros(df_Sales, 'cantidad')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'moneda')
df_Sales = CargaDatos.TextoLimpio(df_Sales, 'tipo_comprobante')

# Carga de JSON
df_Inventory = CargaDatos.Cargar_Json(ruta_crudo + "inventory.json")

if df_Inventory is None:
    raise ValueError("El archivo inventory.json no se pudo cargar correctamente desde S3.")

# Tiendas
df_Tiendas = df_Inventory['dfTiendas']
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
# Primer aplanado del JSON
df_Catalogo_ = CargaDatos.AplanarJson(df_Catalogo, 'productos')
# Segundo aplanado del JSON
df_Cost_History = CargaDatos.SegundoAplanadoJson(df_Catalogo_, 'cost_history')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'sku_erp')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'nombre')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'categoria')
df_Cost_History = CargaDatos.CambioFecha(df_Cost_History, 'fecha_vigencia')
df_Cost_History = CargaDatos.TextoLimpio(df_Cost_History, 'proveedor')

# Carga de archivo parquet
df_Ecommerce = CargaDatos.Cargar_Parquet(ruta_crudo + "ecommerce_orders.parquet")
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
erps_unicos = df_Cost_History['sku_erp'].dropna().unique()

diccionario_sku = {}
for sku in erps_unicos:
    partes = str(sku).split('-')
    if len(partes) > 3:
        clave = partes[3]
        diccionario_sku[clave] = sku

claves_extraidas = df_SKU['sku_pos'].str[-3:]

df_SKU['sku_erp'] = df_SKU['sku_erp'].fillna(claves_extraidas.map(diccionario_sku))

handle_faltante = df_SKU[df_SKU['handle'].isna()]['sku_erp'].unique()

df_nombre_filtrado = df_Cost_History[df_Cost_History['sku_erp'].isin(handle_faltante)].drop_duplicates(subset=['sku_erp']).copy()
df_nombre_filtrado['nombre_limpio'] = (
    df_nombre_filtrado['nombre']
    .str.lower()
    .str.replace(' ', '-', regex=False)
)

df_nombre_filtrado['digitos_finales'] = df_nombre_filtrado['sku_erp'].str.split('-').str[3]
df_nombre_filtrado['handle_generado'] = df_nombre_filtrado['nombre_limpio'] + '-' + df_nombre_filtrado['digitos_finales']

diccionario_handle = df_nombre_filtrado.set_index('sku_erp')['handle_generado'].to_dict()

df_SKU['handle'] = df_SKU['handle'].fillna(df_SKU['sku_erp'].map(diccionario_handle))

df_Ecommerce['customer_rfc'] = df_Ecommerce['customer_rfc'].fillna('XAXX010101000')

print(f"Carga de archivos limpios en formato parquet")
try:
    df_Exchange_rate.to_parquet(ruta_limpio + 'Exchange_Rate.parquet', index=False)
    df_Sales.to_parquet(ruta_limpio + 'Sales.parquet', index=False)
    df_Tiendas.to_parquet(ruta_limpio + 'Tiendas.parquet', index=False)
    df_SKU.to_parquet(ruta_limpio + 'Sku.parquet', index=False)
    df_Cost_History.to_parquet(ruta_limpio + 'Cost_history.parquet', index=False)
    df_Ecommerce.to_parquet(ruta_limpio + "Ecommerce.parquet", index=False)
    print("Archivos cargados con exito, sobre carpeta /limpio/")
except Exception as e:
    print(f"Error al cargar los archivos parquet finales: {e}")