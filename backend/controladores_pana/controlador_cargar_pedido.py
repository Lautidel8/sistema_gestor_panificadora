from backend.conexion_a_BD.conexion_db import conectar

class CargarPedido:
    
    def __init__(self):
        self.conexion = conectar()
        self.conexion.autocommit = False  # manejar transacciones manualmente
        self.cursor = self.conexion.cursor()
    
    def _receta_producto(self, id_producto: int):
        # ...existing code...
        self.cursor.execute(
            """
            SELECT mp.id_materia_prima,
                   mp.nombre_materia_prima,
                   mp.stock,
                   mpp.cantidad
            FROM MateriaPrima_Producto mpp
            JOIN MateriaPrima mp ON mp.id_materia_prima = mpp.id_materia_prima
            WHERE mpp.id_producto = %s
            """,
            (id_producto,)
        )
        return self.cursor.fetchall()

    def _requerimientos_para(self, id_producto: int, cantidad_producto: int):
        # ...existing code...
        receta = self._receta_producto(id_producto)
        req = []
        for row in receta:
            id_mp, nombre, stock, por_unidad = row
            requerido = float(por_unidad) * float(cantidad_producto)
            disponible = float(stock)
            faltante = max(0.0, requerido - disponible)
            req.append(
                {
                    "id_materia_prima": id_mp,
                    "nombre": nombre,
                    "requerido": requerido,
                    "disponible": disponible,
                    "faltante": faltante,
                }
            )
        return req

    def seleccionar_producto(self):
        # ...existing code...
        self.cursor.execute(
            "SELECT id_producto, nombre_producto, precio_unitario FROM Producto ORDER BY nombre_producto"
        )
        return self.cursor.fetchall()
    
    def verificar_cantidad_materia_prima(self, id_producto: int, cantidad: int):
        # ...existing code...
        requerimientos = self._requerimientos_para(id_producto, cantidad)
        faltantes = [r for r in requerimientos if r["faltante"] > 0]
        if faltantes:
            return False, faltantes
        return True, []
    
    def _crear_pedido(self, nombre_pedido: str, cliente: str, fecha_pedido, estado_pedido="Pendiente", id_gerente=None):
        # ...existing code...
        self.cursor.execute(
            """
            INSERT INTO Pedido (nombre_pedido, estado_pedido, cliente, fecha_pedido, id_gerente)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre_pedido, estado_pedido, cliente, fecha_pedido, id_gerente)
        )
        return self.cursor.lastrowid

    def _insertar_detalle(self, id_pedido: int, id_producto: int, cantidad: int):
        # ...existing code...
        self.cursor.execute(
            """
            INSERT INTO Detalle_pedido (id_pedido, id_producto, cantidad)
            VALUES (%s, %s, %s)
            """,
            (id_pedido, id_producto, int(cantidad))
        )

    def _descontar_stock(self, requerimientos: list):
        # ...existing code...
        for r in requerimientos:
            self.cursor.execute(
                "UPDATE MateriaPrima SET stock = stock - %s WHERE id_materia_prima = %s",
                (r["requerido"], r["id_materia_prima"])
            )

    def agregar_producto_a_pedido(self, id_pedido: int, id_producto: int, cantidad: int):
        """
        Quita start_transaction; usa autocommit=False + commit/rollback.
        """
        try:
            ok, faltantes = self.verificar_cantidad_materia_prima(id_producto, cantidad)
            if not ok:
                return {"ok": False, "faltantes": faltantes}

            # No llamar start_transaction aquí
            self._insertar_detalle(id_pedido, id_producto, cantidad)
            req = self._requerimientos_para(id_producto, cantidad)
            self._descontar_stock(req)

            self.conexion.commit()
            return {"ok": True}
        except Exception as e:
            self.conexion.rollback()
            print(f"Error al agregar producto al pedido: {e}")
            return {"ok": False, "error": str(e)}
    
    def cargar_pedido(self, nombre_pedido: str, cliente: str, fecha_pedido, items: list, estado_pedido="Pendiente", id_gerente=None):
        """
        Quita start_transaction; usa autocommit=False + commit/rollback.
        """
        try:
            faltantes_por_producto = {}
            for it in items:
                ok, faltantes = self.verificar_cantidad_materia_prima(it["id_producto"], it["cantidad"])
                if not ok:
                    faltantes_por_producto[it["id_producto"]] = faltantes

            if faltantes_por_producto:
                return {"ok": False, "faltantes": faltantes_por_producto}

            # No llamar start_transaction aquí
            id_pedido = self._crear_pedido(nombre_pedido, cliente, fecha_pedido, estado_pedido, id_gerente)

            for it in items:
                self._insertar_detalle(id_pedido, it["id_producto"], it["cantidad"])
                req = self._requerimientos_para(it["id_producto"], it["cantidad"])
                self._descontar_stock(req)

            self.conexion.commit()
            return {"ok": True, "id_pedido": id_pedido}
        except Exception as e:
            self.conexion.rollback()
            print(f"Error al cargar pedido: {e}")
            return {"ok": False, "error": str(e)}
    
    def cerrar_conexion(self):
        if hasattr(self, "cursor") and self.cursor:
            self.cursor.close()
        if hasattr(self, "conexion") and self.conexion:
            self.conexion.close()