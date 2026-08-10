import pandas as pd
import json


class CargaDatos:

    def __init__(self):
        pass

    # Método para realizar la carga de archivo csv
    def Cargar_CSV(self, ArchivoCSV):
        try:
            df = pd.read_csv(ArchivoCSV)
            print(f"Se realizó la carga de datos correctamente desde el archivo CSV")
            return df
        except FileNotFoundError:
            print(f"No se encontró el archivo {ArchivoCSV}. Por favor, proporcione uno correcto.")
            return None
        except Exception as e:
            print(f"Error al cargar el archivo {ArchivoCSV} debido a {e}")
            return None

    # Método para realizar la carja de archivo JSON y aplanarlo
    def Cargar_Json(self,ArchivoJson):
        try:
            with open(ArchivoJson, 'r', encoding='utf-8') as j:
                datosCrudos = json.load(j)

                TablasJson = {
                    "dfTiendas": pd.DataFrame(datosCrudos['tiendas_info']),
                    "dfSKU": pd.DataFrame(datosCrudos['sku_mappings']),
                    "dfCatalogo": pd.DataFrame(datosCrudos['catalogo']),
                    "dfCorte": pd.DataFrame(datosCrudos['snapshots'])
                }
                print(f"Se realizó la carga de datos correctamente desde el archivo JSON")
                return TablasJson
        except FileNotFoundError:
            print(f"No se encontró el archivo {ArchivoJson}. Por favor, proporcione uno correcto.")
            return None
        except Exception as e:
            print(f"Error al cargar el archivo {ArchivoJson} debido a {e}")
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
            df = pd.read_parquet(ArchivoParquet)
            print(f"Se realizó la carga de datos correctamente desde el archivo Parquet")
            return df
        except FileNotFoundError:
            print(f"No se encontró el archivo {ArchivoParquet}. Por favor, proporcione uno correcto.")
            return None
        except Exception as e:
            print(f"Error al cargar el archivo {ArchivoParquet} debido a {e}")
            return None


    # Método para limpieza de datos


        # Metodo para limpieza de columnas de texto, eliminando caracteres especiales y espacios en blanco
    def TextoLimpio(self, df, columna):
        if columna in df.columns:
                try:
                    if df[columna].dtype == 'object':
                        # Por cuestiones de diferencias en la codificación se borra la opción de eliminar caracteres especiales
                        # df[columna] = df[columna].str.replace(r'[^\w\s\-]', '', regex=True)
                        df[columna] = df[columna].str.strip()
                    else:
                        print(f"La columna {columna} no es de tipo texto")                    
                except Exception as e:
                    print(f"Se tuvo un problema al limpiar la columna {columna}: {e}")
        else:
            print(f"La columna {columna} no existe en el DataFrame")
        return df

    



        # Método para cambiar el tipo de dato a entero
    def CambioEnteros(self,df, columna):
        if columna in df.columns:
            try:
                if df[columna].dtype != 'Int64':
                    df[columna] = pd.to_numeric(df[columna], errors='coerce').astype('Int64')
                else:
                    print(f"La columna {columna} ya es de tipo entero")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a entero: {e}")
        else:
            print(f"La columna {columna} no existe en el DataFrame")
        return df



    

        # Método para cambiar el tipo de dato a flotante
    def CambioFlotantes(self,df, columna):
        if columna in df.columns:
            try:
                if df[columna].dtype != 'float64':
                    df[columna] = pd.to_numeric(df[columna], errors='coerce').astype('float64')
                else:
                    print(f"La columna {columna} ya es de tipo flotante")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a flotante: {e}")
        else:
            print(f"La columna {columna} no existe en el DataFrame")
        return df


    
        # Metodo para cambiar el tipo de dato a fecha
    def CambioFecha(self,df, columna):
        if columna in df.columns:
            try:
                if not pd.api.types.is_datetime64_any_dtype(df[columna]):
                    df[columna] = pd.to_datetime(df[columna], errors='coerce')
                else:
                    print(f"La columna {columna} ya es de tipo fecha")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a fecha: {e}")
        else:
            print(f"La columna {columna} no existe en el DataFrame")
        return df




        # Metodo para cambiar el tipo de dato a string

    def CambioString(self,df, columna):
        if columna in df.columns:
            try:
                if df[columna].dtype != 'object':
                    df[columna] = df[columna].astype(str)
                else:
                    print(f"La columna {columna} ya es de tipo string")
            except Exception as e:
                print(f"Se tuvo un problema al cambiar la columna {columna} a string: {e}")
        else:
            print(f"La columna {columna} no existe en el DataFrame")
        return df
