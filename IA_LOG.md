# IA LOG -- BITÁCORA DE USO


## 1. Herramientas Utilizadas

Modelo / Asistente: Google Gemini

Entorno de desarrollo: Visual Studio Code (VS Code) con Python 3.12, Pandas, S3FS y AWS (Athena / Glue).


## 2. Flujo de Trabajo y Orquestación

Orquestación: No se utulizó agentes autónomos, el uso fue guiado por las decisiones de negocio y técnicas que definí, así como el diseño de la arquitectura que tendría la tubería. La IA brindó el apoyo como un guía de ingeniería y de documentación.



## 3. Pompts 

Los siguentes prompt se obtuvieron dentro de la conversación que se tuvon con GEMINI

**1**

Prompt que escribí (resumido) : “Tengo esto para mi README: Pipeline de Ingestión Multi-Formato... [texto base]... ¿Qué me recomiendas que ponga?”

Lo que devolvió la IA (resumido):
Una estructura profesional en Markdown dividiendo el proyecto con distintivos visuales, badges, la lista exacta de dependencias (Pandas, S3FS), el mapa de la estructura de archivos del repositorio y bloques claros para las preguntas de negocio.

Qué hice: Corregí manualmente la sección de tecnología (cambiando el framework Anaconda por el uso real de Python 3 y VS Code) y ajusté el enfoque técnico como un flujo ELT en lugar de ETL

**2**
Prompt que escribí: “Quiero agregar este diagrama a esa propuesta sobre qué es lo que hará como tal, todo antes de que se haga la migración a spark o se agreguen Eventos y Lambdas. Me ayudas a digitalizarlo (referencia al diagrama dibujado a mano con 8 pasos).”

Lo que devolvió la IA (resumido): Una propuesta de estructura en bloques organizada exactamente en 8 pasos numerados (desde la PC local, pasando por S3 crudo, Glue, Pandas, S3 limpio, Athena, CTAS y reportes finales).

Qué hice: El primer intento de la IA generó un diagrama en cascada y posterior uno con formato libre. Le hice una corrección estricta pidiendo un recuadrio visual enumerado con el tipo arquitectura de AWS. El resultado final encajó perfectamente con el esquema que había diseñado.


**3**
Prompt que escribí: Tengo cargados mis datasets... necesito resolver estas 4 preguntas de negocio específicas con estas restricciones técnicas (CTAS, Parquet, Athena)... dame la estructura.

Lo que devolvió la IA (resumido):Las 4 consultas SQL estructuradas para Athena utilizando instrucciones CREATE TABLE AS SELECT (CTAS) para persistir los resultados optimizados en formato Apache Parquet dentro de S3. Incluyó la estrategia de unificación de canales con UNION ALL, el uso de funciones de ventana con LAG() particionadas por tienda y SKU para la detección de desabastos consecutivos, el cálculo de crecimiento mes a mes con manejo defensivo de nulos mediante NULLIF(), y un cruce temporal condicional (BETWEEN) contra la tabla de costos históricos para garantizar la precisión en el análisis de márgenes y salud financiera.


Que hice: Con base a eso se utilicé la redacción y optimización de los querys en Athena, valide la información y ajusté los campos para que se guadaran en el bucket requeriido.


## 4 Caso de Error de la IA

Durante uno de los prompts comenzó a soltar información respecto a una arquitectura muy compleja la cual veía muy compleja manejando una división cumputacional con Spark

Como lo detecte: Cuando sugierió el uso de ERM o de clusters virtuales.

Como se corrigió: Al verificar el tamaño de los datos, las columnas, filas y haciendo un pequeño calculo de los datos noté que sobre mi computadora local podía correrlos sin problemas, así que se descartó ese sugerencia que arrojó.


## Autocirtica 

Al final, la misma arquitectura ya la tenía planeado, al igual que su clase con sus funciones, la IA me sirvió como apoyo con manejo de errores, guía en interfaces de nube, consultas de sql así como la documentación. Si tuviera que colocarlo con porcentaje yo estimo que un 75% es mío y un 25% IA. La forma de validarlo fue observando los df verificando validando nulos, borrando espacios, llenando datos faltantes y sin olvidar las consulas verificando la coherencia.