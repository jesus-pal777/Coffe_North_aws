CREATE TABLE reporte_quiebres_stock 
WITH (
    format = 'PARQUET',
    external_location = 's3://ruta_a_guardar_querys'
) AS 
WITH max_fecha AS (
    -- Obtenemos la fecha más reciente real que existe en tus datos
    SELECT MAX(fecha_hora) AS ultima_venta FROM sales
),
ventas_por_dia AS (
    SELECT DISTINCT
        v.tienda_id,
        v.sku,
        date(v.fecha_hora) AS fecha_venta
    FROM sales v, max_fecha m
    -- Filtramos los últimos 3 meses hacia atrás a partir de la última venta real de tus datos
    WHERE v.fecha_hora >= m.ultima_venta - interval '3' month
),
ventas_con_lag AS (
    SELECT 
        tienda_id,
        sku,
        fecha_venta,
        LAG(fecha_venta, 1) OVER (PARTITION BY tienda_id, sku ORDER BY fecha_venta) AS fecha_anterior
    FROM ventas_por_dia
),
diferencia_dias AS (
    SELECT 
        tienda_id,
        sku,
        fecha_anterior,
        fecha_venta,
        date_diff('day', fecha_anterior, fecha_venta) AS dias_sin_venta
    FROM ventas_con_lag
)
SELECT DISTINCT
    t.tienda_id,
    t.ciudad,
    t.region,
    d.sku,
    d.dias_sin_venta
FROM diferencia_dias d
JOIN tiendas t ON d.tienda_id = t.tienda_id
WHERE d.dias_sin_venta > 3
ORDER BY d.dias_sin_venta DESC;
