# Arquitectura en AWS para proceso ELT Multi-formato


## PROPUESTA DE ARQUITECTURA DE DATOS EN NUBE ORIENTADA A EMPRESAS PyME CON FLUJO DE DATOS MODERADOS, DISEÑADO CON UN ENFOQUE ELT. LA TUBERÍA AUTOMATIZA LA INGESTA EN LA NUBE PERMITIENDO CONSULTAS SQL PARA PREGUNTAS DE NEGOCIO DE FORMA ESCALABLE Y FUNCIONAL.


## Tecnologías y Entorno

* **Lenguaje:** Python 3.12
* **Librerías:** Pandas (procesamiento de datos), json (manipulación y lectura de Json), s3fs (conexión y lectura desde Amazon S3)
* **Entorno:** Se utilizó un entorno de Anaconda para asegurar la gestión de dependencias y aislamiento de versiones.
* **Almacenamiento y Cloud:**: Amazon S3 (AWS)
* **Motor de consulta:**: Amazon Athena



## Preguntas de Negocio 

* Una vez cargados nuestros datos el pipeline ejecuta consultas analíticas para resolver cuatro cuestiones criticas del negocio:


### 1. Inventario con Top 10 SKUs más vendidos
* **Objetivo:** Identificar los 10 productos con mayor índice de rotación en los últimos 6 meses.
* **Enfoque técnico:** Manipulación de series de tiempo, agregaciones y filtros sobre el DF generado.

### 2. Quiebres en Stock por 3 días consecutivos
* **Objetivo:** Detectar las tiendas físicas o virtuales que sufrieron desabasto por un periodo de 3 días consecutivos durante el último trimestre.
* **Enfoque técnico:** Implementación de métodos de desplazamiento de datos y lógica de agrupación para medir el desabasto consecutivo.

### 3. Crecimiento Mes a Mes Tienda Física vs E-Commerce
* **Objetivo:** Calcular el crecimiento mes a mes de las ventas en Tienda Física vs. E-Commerce durante el último año.
* **Enfoque técnico:** Extracción de componentes de tipo fecha, agrupaciones cruzadas y comparando el mes en curso con el mes anterior.

### 4. Salud Financiera en empresa
* **Objetivo:** Identificar qué productos generaron pérdidas.
* **Enfoque técnico:** Operaciones aritméticas entre columnas comparando costo/precio