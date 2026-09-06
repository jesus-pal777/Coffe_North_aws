CREATE TABLE reporte_margen_negativo 
WITH (
    format = 'PARQUET',
    external_location = 's3://ruta_a_guardar_querys'
) AS 
WITH costos_vigentes AS (
    SELECT 
        s.venta_id,
        s.tienda_id,
        s.sku AS sku_pos,
        sk.sku_erp,
        s.cantidad,
        s.monto AS monto_total_venta,
        -- Calculamos el precio unitario real de venta (evitando división por cero)
        (s.monto / NULLIF(s.cantidad, 0)) AS precio_unitario_venta,
        ch.costo_mxn AS costo_unitario,
        ch.nombre,
        s.fecha_hora
    FROM sales s
    -- Cruzamos el POS con el ERP
    JOIN sku sk ON s.sku = sk.sku_pos
    -- Cruzamos con el histórico evaluando la vigencia de la fecha
    JOIN costhistory ch ON sk.sku_erp = ch.sku_erp
    WHERE s.fecha_hora >= ch.fecha_vigencia
)
SELECT DISTINCT
    c.tienda_id,
    t.ciudad,
    t.region,
    c.sku_erp,
    c.nombre AS nombre_producto,
    c.precio_unitario_venta,
    c.costo_unitario,
    -- Margen unitario (resultado negativo = pérdida)
    (c.precio_unitario_venta - c.costo_unitario) AS margen_unitario
FROM costos_vigentes c
JOIN tiendas t ON c.tienda_id = t.tienda_id
-- REGLA DE NEGOCIO: Filtrar únicamente donde el costo supere al precio de venta
WHERE c.costo_unitario > c.precio_unitario_venta
ORDER BY margen_unitario ASC;
