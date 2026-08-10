CREATE TABLE reporte_crecimiento_mom 
WITH (
    format = 'PARQUET',
    external_location = 's3://amz-coffenorth-data/resultados/QuerysPrincipales/Crecimiento_MoM/'
) AS 
WITH ventas_fisicas_mxn AS (
    SELECT 
        date_format(fecha_hora, '%Y-%m') AS anio_mes,
        'Físico (POS)' AS canal,
        SUM(monto) AS total_venta_mxn
    FROM sales
    WHERE fecha_hora >= current_date - interval '1' year
    GROUP BY date_format(fecha_hora, '%Y-%m')
),
ventas_ecom_convertidas AS (
    SELECT 
        e.order_id,
        date_format(e.fecha, '%Y-%m') AS anio_mes,
        'E-commerce' AS canal,
        CASE 
            WHEN e.currency = 'MXN' THEN e.amount
            ELSE e.amount * COALESCE(ex.rate_to_mxn, 1.0)
        END AS monto_mxn
    FROM ecommerce e
    LEFT JOIN exchangerate ex 
        ON date(e.fecha) = date(ex.fecha) 
        AND e.currency = ex.currency
    WHERE e.fecha >= current_date - interval '1' year
),
ventas_ecom_mxn AS (
    SELECT 
        anio_mes,
        canal,
        SUM(monto_mxn) AS total_venta_mxn
    FROM ventas_ecom_convertidas
    GROUP BY anio_mes, canal
),
unificado AS (
    SELECT * FROM ventas_fisicas_mxn
    UNION ALL
    SELECT * FROM ventas_ecom_mxn
),
con_mes_anterior AS (
    SELECT 
        anio_mes,
        canal,
        total_venta_mxn,
        LAG(total_venta_mxn, 1) OVER (PARTITION BY canal ORDER BY anio_mes) AS venta_mes_anterior
    FROM unificado
)
SELECT 
    anio_mes,
    canal,
    total_venta_mxn,
    venta_mes_anterior,
    CASE 
        WHEN venta_mes_anterior IS NULL OR venta_mes_anterior = 0 THEN NULL
        ELSE ROUND(((total_venta_mxn - venta_mes_anterior) / venta_mes_anterior) * 100, 2)
    END AS crecimiento_mom_porcentaje
FROM con_mes_anterior
ORDER BY canal, anio_mes;