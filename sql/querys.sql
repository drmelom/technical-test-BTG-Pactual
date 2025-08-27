SELECT DISTINCT c.nombre
FROM btg.cliente c
JOIN btg.cliente_producto cp ON c.id_cliente = cp.id_cliente
JOIN btg.producto p ON cp.id_producto = p.id_producto
-- sucursales que el cliente visita
JOIN btg.cliente_sucursal cs ON c.id_cliente = cs.id_cliente
-- productos disponibles en esas sucursales
JOIN btg.sucursal_producto sp ON p.id_producto = sp.id_producto
                              AND cs.id_sucursal = sp.id_sucursal
WHERE NOT EXISTS (
    -- Excluir productos que estén en sucursales que el cliente NO visita
    SELECT 1
    FROM btg.sucursal_producto sp2
    WHERE sp2.id_producto = p.id_producto
      AND sp2.id_sucursal NOT IN (
          SELECT cs2.id_sucursal
          FROM btg.cliente_sucursal cs2
          WHERE cs2.id_cliente = c.id_cliente
      )
);
