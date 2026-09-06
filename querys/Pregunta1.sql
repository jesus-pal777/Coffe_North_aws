CREATE TABLE reporte_top_skus 
WITH (
    format = 'PARQUET',
    external_location = 's3://ruta_a_guardar_querys'
) AS
WITH ventas_unificadas AS (
    -- Ventas físicas (POS)
    SELECT 
        s.sku_erp AS sku_erp,
        v.fecha_hora AS fecha,
        v.cantidad
    FROM sales v
    JOIN sku s ON v.sku = s.sku_pos
    
    UNION ALL
    
    -- Ventas e-commerce
    SELECT 
        s.sku_erp AS sku_erp,
        e.fecha AS fecha,
        e.cantidad
    FROM ecommerce e
    JOIN sku s ON e.product_handle = s.handle
),
rotacion_skus AS (
    SELECT 
        v.sku_erp,
        SUM(v.cantidad) AS total_unidades_vendidas
    FROM ventas_unificadas v
    WHERE v.fecha >= current_date - interval '6' month
    GROUP BY v.sku_erp
)
SELECT 
    r.sku_erp,
    ch.nombre,
    ch.categoria,
    r.total_unidades_vendidas
FROM rotacion_skus r
JOIN (
    SELECT DISTINCT sku_erp, nombre, categoria 
    FROM costhistory
) ch ON r.sku_erp = ch.sku_erp
ORDER BY total_unidades_vendidas DESC
LIMIT 10;
