from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
import flet as ft
from datetime import datetime
from backend.util_paths import resource_path

class vista_principal(configuracion_pantalla):
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.pedido_seleccionado = None
        self.pedido_guardado = None
        self.pedidos_refresh = [] 
        self.data_table = None 
        self.totales_map = {}
        self.rows_container = None
        self.config_page()
        self.armar_vista()


    def seleccionar_pedido(self, e, pedido):
        if getattr(e, "data", None) is False:
            self.pedido_seleccionado = None
        else:
            if self.pedido_seleccionado is not None and self.pedido_seleccionado[0] == pedido[0]:
                self.pedido_seleccionado = None
            else:
                self.pedido_seleccionado = pedido

        self._refresh_table()
        self.page.update()
        
        
    def _load_totales(self):
        """
        Carga en self.totales_map el total por pedido:
        SUM(Detalle_pedido.cantidad * Producto.precio_unitario)
        """
        try:
            self.cursor.execute(
                """
                SELECT dp.id_pedido, SUM(dp.cantidad * p.precio_unitario) as total
                FROM Detalle_pedido dp
                JOIN Producto p ON dp.id_producto = p.id_producto
                GROUP BY dp.id_pedido
                """
            )
            rows = self.cursor.fetchall()
            self.totales_map = {r[0]: (r[1] if r[1] is not None else 0) for r in rows}
        except Exception:
            self.totales_map = {}
        
    def _refresh_table(self):
        if not self.rows_container:
            return
        
        self._load_totales()
        
        rows = []
        for pedido in self.pedidos_refresh:
            pid = pedido[0]
            selected = (self.pedido_seleccionado is not None and self.pedido_seleccionado[0] == pid)
            total = self.totales_map.get(pid, 0)
            total_display = f"{total:,.2f}" if isinstance(total, (int, float)) else str(total)

            bg = "#ffc7a4" if selected else None
        
            rows.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(ft.Text(str(pedido[1]), style=self.estilo_texto()), expand=True, padding=10),
                            ft.Container(ft.Text(str(pedido[3]), style=self.estilo_texto()), expand=True, padding=10),
                            ft.Container(ft.Text(str(pedido[4]), style=self.estilo_texto()), expand=True, padding=10),
                            ft.Container(ft.Text(total_display, style=self.estilo_texto()), expand=True, padding=10),
                            ft.Container(ft.Text(str(pedido[2]), style=self.estilo_texto()), expand=True, padding=10),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    ),
                    bgcolor=bg,
                    on_click=lambda e, pedido=pedido: self.seleccionar_pedido(e, pedido)
                )
            )
            
        self.rows_container.controls = rows
        self.page.update()
        
    def filtrar_por_fecha(self, fecha):
        if not fecha:
            return
            
        fecha_str = fecha.strftime('%Y-%m-%d')
        
        if not hasattr(self, 'pedidos_originales'):
            self.pedidos_originales = self.pedidos_refresh.copy()

        self.pedidos_refresh = [p for p in self.pedidos_originales if str(p[4]) == fecha_str]

        self._refresh_table()
        self.page.update()

        self.mostrar_snack_bar(f"Mostrando pedidos del {fecha_str}")

    def limpiar_filtro(self):
        """Limpia el filtro y muestra todos los pedidos"""
        if hasattr(self, 'pedidos_originales'):
            self.pedidos_refresh = self.pedidos_originales.copy()
            self._refresh_table()
            self.page.update()
            
            self.mostrar_snack_bar("Filtro limpiado, mostrando todos los pedidos")

    def mostrar_ventana_modificar_producto(self):
        from backend.controladores_pana.control_cargar_producto import control_cargar_producto

        ctrl = control_cargar_producto()
        try:
            productos = ctrl.listar_productos()
        except Exception as e:
            print(f"Error listando productos: {e}")
            productos = []

        dd_productos = ft.Dropdown(
            label="Producto",
            width=320,
            options=[ft.dropdown.Option(key=str(p[0]), text=p[1]) for p in productos],
            label_style=self.estilo_texto(),
            focused_border_color="#807E7E",
            color="#37373A",
            hint_style=self.estilo_texto(),
        )
        tf_nombre = ft.TextField(
            label="Nuevo nombre",
            width=320,
            label_style=self.estilo_texto(),
            text_style=self.estilo_texto(),
            focused_border_color="#807E7E",
            color="#37373A",
            hint_style=self.estilo_texto(),
        )
        tf_precio = ft.TextField(
            label="Precio unitario",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*(?:[.,]\d*)?$"),
            label_style=self.estilo_texto(),
            text_style=self.estilo_texto(),
            focused_border_color="#807E7E",
            color="#37373A",
            hint_style=self.estilo_texto(),
        )

        def cargar_datos_producto(e):
            if not dd_productos.value:
                return
            pid = int(dd_productos.value)
            prod = ctrl.obtener_producto_por_id(pid)
            if prod:
                tf_nombre.value = prod[1] or ""
                tf_precio.value = str(prod[2] or "")
                self.page.update()

        dd_productos.on_change = cargar_datos_producto

        def guardar_cambios(e):
            if not dd_productos.value:
                self.mostrar_snack_bar("Selecciona un producto")
                return
            if not tf_nombre.value.strip():
                self.mostrar_snack_bar("Ingresa un nombre")
                return
            if not tf_precio.value.strip():
                self.mostrar_snack_bar("Ingresa un precio")
                return
            try:
                # permitir coma o punto
                nuevo_precio = float(tf_precio.value.replace(",", "."))
            except ValueError:
                self.mostrar_snack_bar("El precio debe ser numérico")
                return

            pid = int(dd_productos.value)
            res = ctrl.actualizar_producto(pid, tf_nombre.value.strip(), nuevo_precio)
            if res is True:
                self.mostrar_snack_bar("Producto actualizado")
                dlg.open = False
                # refrescar totales en la grilla para ver el nuevo precio aplicado
                self._load_totales()
                self._refresh_table()
                self.page.update()
            elif res == "duplicado":
                self.mostrar_snack_bar("Ya existe un producto con ese nombre")
            else:
                self.mostrar_snack_bar("Error al actualizar producto")

        contenido = ft.Container(
            width=520,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("Seleccione el prodcuto que desee modificar", size=16, weight="bold", style=self.estilo_texto()),
                    dd_productos,
                    tf_nombre,
                    tf_precio,
                ],
            ),
        )

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor="#fdd0b5",
            title=ft.Text("Modificar producto", style=self.estilo_texto(), size=25),
            content=contenido,
            actions=[
                ft.TextButton("Cancelar", style=self.estilo_de_botones(), on_click=lambda e: (setattr(dlg, "open", False), self.page.update())),
                ft.TextButton("Guardar", style=self.estilo_de_botones(), on_click=guardar_cambios),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: ctrl.cerrar_conexion(),
        )

        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()    
            
            
    def mostrar_ventana_cargar_pedido(self):
        
        import flet as ft
        from datetime import date
        from backend.controladores_pana.controlador_cargar_pedido import CargarPedido

        estado = {
            "items": [],               
            "productos": [],           
            "total": 0.0,
        }

        controlador = CargarPedido()
        try:
            estado["productos"] = controlador.seleccionar_producto()
        except Exception as e:
            print(f"Error cargando productos: {e}")
            estado["productos"] = []

        prod_por_id = {str(p[0]): p for p in estado["productos"]}


        tf_nombre = ft.TextField(label="Nombre del pedido", width=250, label_style=self.estilo_texto(), text_style=self.estilo_texto(),focused_border_color="#807E7E",color="#37373A",hint_style=self.estilo_texto())
        tf_cliente = ft.TextField(label="Cliente", width=250, label_style=self.estilo_texto(), text_style=self.estilo_texto(),focused_border_color="#807E7E",color="#37373A",hint_style=self.estilo_texto())
        fecha_label = ft.Text(str(date.today()), style=self.estilo_texto())
        date_picker = ft.DatePicker(on_change=lambda e: (setattr(fecha_label, "value", str(e.control.value)), self.page.update()))

        dd_productos = ft.Dropdown(
            label="Producto",
            width=320,
            options=[
                ft.dropdown.Option(text=f"{p[1]} - ${float(p[2]):,.2f}", key=str(p[0])) for p in estado["productos"]
            ],
            label_style=self.estilo_texto(),focused_border_color="#807E7E",color="#37373A",hint_style=self.estilo_texto()
        )
        tf_cantidad = ft.TextField(
            label="Cantidad",
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            # permite "", "12", "12.", ".5", "12,5"
            input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*(?:[.,]\d*)?$"),
            label_style=self.estilo_texto(),
            text_style=self.estilo_texto(),
            focused_border_color="#807E7E",
            color="#37373A",
            hint_style=self.estilo_texto()
        )

        lista_items = ft.Column(spacing=6, scroll="auto", height=180)
        txt_total = ft.Text("Total: $ 0.00", weight="bold", style=self.estilo_texto())

        def recalcular_total():
            total = 0.0
            for it in estado["items"]:
                total += float(it["precio"]) * float(it["cantidad"])
            estado["total"] = total
            txt_total.value = f"Total: $ {total:,.2f}"

        def actualizar_lista():
            lista_items.controls.clear()
            for idx, it in enumerate(estado["items"]):
                fila = ft.Container(
                    bgcolor="#fcc8a9",
                    border_radius=6,
                    padding=8,
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{it['nombre']} x {it['cantidad']} u", style=self.estilo_texto()),
                            ft.Text(f"$ {float(it['precio']):,.2f}", style=self.estilo_texto()),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="#a72d2d",
                                tooltip="Quitar",
                                on_click=lambda e, i=idx: quitar_item(i),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                )
                lista_items.controls.append(fila)
            recalcular_total()
            self.page.update()

        def quitar_item(idx):
            if 0 <= idx < len(estado["items"]):
                estado["items"].pop(idx)
                actualizar_lista()

        def agregar_item(e):
            if not dd_productos.value:
                self.mostrar_snack_bar("Selecciona un producto")
                return
            if not tf_cantidad.value or tf_cantidad.value.strip() == "":
                self.mostrar_snack_bar("Ingresa una cantidad")
                return
            try:
                cant = float(tf_cantidad.value.replace(",", "."))
                if cant <= 0:
                    raise ValueError
            except ValueError:
                self.mostrar_snack_bar("La cantidad debe ser un número positivo")
                return

            p = prod_por_id.get(dd_productos.value)
            if not p:
                self.mostrar_snack_bar("Producto inválido")
                return

            id_prod, nombre, precio = p[0], p[1], float(p[2])

            ok, faltantes = controlador.verificar_cantidad_materia_prima(id_prod, cant)
            if not ok:
                msg = "Faltan insumos:\n" + "\n".join(
                    [f"- {f['nombre']}: falta {f['faltante']:.2f}" for f in faltantes]
                )
                self.mostrar_snack_bar(msg)
                return

            estado["items"].append({
                "id_producto": id_prod,
                "nombre": nombre,
                "cantidad": cant,
                "precio": precio,
            })
            tf_cantidad.value = ""
            dd_productos.value = None
            actualizar_lista()

        def guardar_pedido(e):
            if not tf_nombre.value or not tf_cliente.value:
                self.mostrar_snack_bar("Completa nombre y cliente")
                return
            if not estado["items"]:
                self.mostrar_snack_bar("Agrega al menos un producto")
                return

            fecha_val = str(date.today()) if not date_picker.value else str(date_picker.value)
            items_payload = [{"id_producto": it["id_producto"], "cantidad": it["cantidad"]} for it in estado["items"]]

            res = controlador.cargar_pedido(
                nombre_pedido=tf_nombre.value.strip(),
                cliente=tf_cliente.value.strip(),
                fecha_pedido=fecha_val,
                items=items_payload,
                estado_pedido="Pendiente",
                id_gerente=None,
            )

            if res.get("ok"):
                try:
                    self.cursor.execute("SELECT * FROM Pedido")
                    self.pedidos_refresh = self.cursor.fetchall()
                except Exception as ex:
                    print(f"Error refrescando pedidos: {ex}")

                self._refresh_table()
                self.mostrar_snack_bar("Pedido cargado con éxito")
                dlg.open = False
                try:
                    controlador.cerrar_conexion()
                except Exception:
                    pass
                self.page.update()
            else:
                if "faltantes" in res:
                    msg = "No hay stock suficiente para:\n"
                    for idp, falt in res["faltantes"].items():
                        nom = next((p[1] for p in estado["productos"] if p[0] == idp), f"Producto {idp}")
                        msg += f"- {nom}:\n"
                        for f in falt:
                            msg += f"   · {f['nombre']}: falta {f['faltante']:.2f}\n"
                    self.mostrar_snack_bar(msg)
                else:
                    self.mostrar_snack_bar("Error al cargar el pedido")
                    

        contenido = ft.Container(
            width=650,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Cargar un nuevo pedido", size=16, weight="bold", style=self.estilo_texto()),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            tf_nombre,
                            tf_cliente,
                            ft.TextButton("Seleccionar fecha", style=self.estilo_de_botones(), on_click=lambda _: self.page.open(date_picker)),
                            fecha_label,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            dd_productos,
                            tf_cantidad,
                            ft.ElevatedButton("Agregar producto", style=self.estilo_de_botones(), on_click=agregar_item),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    lista_items,
                    ft.Row(
                        controls=[txt_total],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
            ),
        )

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor="#fdd0b5",
            title=ft.Text("Cargar pedido", style=self.estilo_texto(), size=25),
            content=contenido,
            actions=[
                ft.TextButton("Cancelar", style=self.estilo_de_botones(), on_click=lambda e: (setattr(dlg, "open", False), controlador.cerrar_conexion(), self.page.update())),
                ft.TextButton("Guardar", style=self.estilo_de_botones(), on_click=guardar_pedido),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.clear()
        self.page.overlay.append(dlg)
        self.page.overlay.append(date_picker)
        dlg.open = True
        self.page.update()

    def mostrar_ventana_modificar_pedido(self):

        if not self.pedido_seleccionado:
            self.mostrar_snack_bar("Selecciona un pedido primero.")
            return

        pedido = self.pedido_seleccionado
        id_pedido = int(pedido[0])
        nombre_actual = str(pedido[1] or "")
        estado_actual = str(pedido[2] or "Pendiente")
        cliente_actual = str(pedido[3] or "")
        fecha_actual = str(pedido[4] or datetime.today().date())


        self.cursor.execute(
            """
            SELECT dp.id_producto, p.nombre_producto, dp.cantidad
            FROM Detalle_pedido dp
            JOIN Producto p ON p.id_producto = dp.id_producto
            WHERE dp.id_pedido = %s
            """,
            (id_pedido,)
        )
        detalle = self.cursor.fetchall()
        
        from backend.controladores_pana.controlador_cargar_pedido import CargarPedido
        ctrl = CargarPedido()
        try:
            catalogo = ctrl.seleccionar_producto()
        finally:
            ctrl.cerrar_conexion()

        estado = {
            "original": {int(r[0]): float(r[2]) for r in detalle},
            "items": [{"id": int(r[0]), "nombre": r[1], "cantidad": float(r[2])} for r in detalle],
            "catalogo": {str(p[0]): (int(p[0]), p[1], float(p[2])) for p in catalogo},
        }

        # Controles cabecera
        tf_nombre = ft.TextField(label="Nombre pedido", value=nombre_actual, width=250, label_style=self.estilo_texto(), text_style=self.estilo_texto(), focused_border_color="#807E7E", color="#37373A", hint_style=self.estilo_texto())
        tf_cliente = ft.TextField(label="Cliente", value=cliente_actual, width=250, label_style=self.estilo_texto(), text_style=self.estilo_texto(), focused_border_color="#807E7E", color="#37373A", hint_style=self.estilo_texto())
        dd_estado = ft.Dropdown(
            label="Estado",
            value=estado_actual if estado_actual in ["Pendiente", "Entregado", "Cancelado"] else "Pendiente",
            options=[ft.dropdown.Option("Pendiente"), ft.dropdown.Option("Entregado"), ft.dropdown.Option("Cancelado")],
            width=200,
            label_style=self.estilo_texto(),
            focused_border_color="#807E7E",
            color="#37373A",
            hint_style=self.estilo_texto(),
        )

        fecha_label = ft.Text(str(fecha_actual), style=self.estilo_texto())
        date_picker = ft.DatePicker(on_change=lambda e: (setattr(fecha_label, "value", str(e.control.value)), self.page.update()))

        # Lista de ítems editables
        lista_items = ft.Column(spacing=6, scroll="auto", height=240)

        def redibujar_items():
            lista_items.controls.clear()
            for idx, it in enumerate(estado["items"]):
                fila = ft.Container(
                    bgcolor="#fcc8a9",
                    border_radius=6,
                    padding=8,
                    content=ft.Row(
                        controls=[
                            ft.Text(it["nombre"], style=self.estilo_texto(), expand=True),
                            ft.TextField(
                                value=str(it["cantidad"]),
                                width=120,
                                keyboard_type=ft.KeyboardType.NUMBER,
                                input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*(?:[.,]\d*)?$"),
                                label="Cantidad",
                                label_style=self.estilo_texto(),
                                text_style=self.estilo_texto(),
                                focused_border_color="#807E7E",
                                color="#37373A",
                                hint_style=self.estilo_texto(),
                                on_change=lambda e, i=idx: actualizar_cantidad(i, e.control.value),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,  # corregido
                                icon_color="#a72d2d",
                                tooltip="Quitar producto",
                                on_click=lambda e, i=idx: quitar_item(i),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                )
                lista_items.controls.append(fila)
            self.page.update()


        def actualizar_cantidad(idx, valor):
            try:
                v = valor.replace(",", ".")
                cant = float(v) if v.strip() not in ("", ".") else 0.0
                if cant < 0:
                    raise ValueError
                estado["items"][idx]["cantidad"] = cant
            except ValueError:
                self.mostrar_snack_bar("Cantidad inválida")

        def quitar_item(idx):
            if 0 <= idx < len(estado["items"]):
                estado["items"].pop(idx)
                redibujar_items()

        redibujar_items()

        dd_productos = ft.Dropdown(
            label="Producto",
            width=320,
            options=[ft.dropdown.Option(key=str(pid), text=nombre) for pid, nombre, _ in catalogo],
            label_style=self.estilo_texto(), focused_border_color="#807E7E", color="#37373A", hint_style=self.estilo_texto()
        )
        tf_cantidad_nueva = ft.TextField(
            label="Cantidad",
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*(?:[.,]\d*)?$"),
            label_style=self.estilo_texto(),
            text_style=self.estilo_texto(),
            focused_border_color="#807E7E",
            color="#37373A",
            hint_style=self.estilo_texto()
        )

        def agregar_item_nuevo(e):
            if not dd_productos.value:
                self.mostrar_snack_bar("Selecciona un producto")
                return
            if not tf_cantidad_nueva.value.strip():
                self.mostrar_snack_bar("Ingresa una cantidad")
                return
            try:
                cant = float(tf_cantidad_nueva.value.replace(",", "."))
                if cant <= 0:
                    raise ValueError
            except ValueError:
                self.mostrar_snack_bar("La cantidad debe ser positiva")
                return

            pid, nombre, _ = estado["catalogo"][dd_productos.value]
            
            for it in estado["items"]:
                if it["id"] == pid:
                    it["cantidad"] += cant
                    break
            else:
                estado["items"].append({"id": pid, "nombre": nombre, "cantidad": cant})

            dd_productos.value = None
            tf_cantidad_nueva.value = ""
            redibujar_items()

        
        def receta_producto(pid: int):
            self.cursor.execute(
                """
                SELECT mp.id_materia_prima, mp.nombre_materia_prima, mp.stock, mpp.cantidad
                FROM MateriaPrima_Producto mpp
                JOIN MateriaPrima mp ON mp.id_materia_prima = mpp.id_materia_prima
                WHERE mpp.id_producto = %s
                """,
                (pid,)
            )
            return self.cursor.fetchall()

        def verificar_incrementos(deltas_por_producto: dict):
            requeridos_por_mp = {}
            nombres_mp = {}
            for pid, delta in deltas_por_producto.items():
                if delta <= 0:
                    continue
                for id_mp, nom_mp, stock, cant_unidad in receta_producto(pid):
                    requerido = float(cant_unidad) * float(delta)
                    requeridos_por_mp[id_mp] = requeridos_por_mp.get(id_mp, 0.0) + requerido
                    nombres_mp[id_mp] = nom_mp
            faltantes = []
            for id_mp, req in requeridos_por_mp.items():
                self.cursor.execute("SELECT stock FROM MateriaPrima WHERE id_materia_prima=%s", (id_mp,))
                fila = self.cursor.fetchone()
                disponible = float(fila[0]) if fila and fila[0] is not None else 0.0
                if req > disponible + 1e-9:
                    faltantes.append({"nombre": nombres_mp[id_mp], "faltante": req - disponible})
            return (len(faltantes) == 0, faltantes)

        def ajustar_stock_por_delta(pid: int, delta: float):
            if abs(delta) <= 1e-9:
                return
            signo = -1.0 if delta > 0 else 1.0
            factor = abs(delta)
            for id_mp, _, _, cant_unidad in receta_producto(pid):
                variacion = signo * (float(cant_unidad) * factor)
                self.cursor.execute(
                    "UPDATE MateriaPrima SET stock = stock + %s WHERE id_materia_prima = %s",
                    (variacion, id_mp)
                )
        
        def eliminar_pedido_confirmado(confirm_dlg):
            try:
                self.cursor.execute(
                    "SELECT id_producto, cantidad FROM Detalle_pedido WHERE id_pedido = %s",
                    (id_pedido,)
                )
                detalle_actual = self.cursor.fetchall()

                for id_prod, cant_prod in detalle_actual:
                    for id_mp, _, _, cant_unidad in receta_producto(id_prod):
                        devolver = float(cant_unidad) * float(cant_prod)
                        self.cursor.execute(
                            "UPDATE MateriaPrima SET stock = stock + %s WHERE id_materia_prima = %s",
                            (devolver, id_mp)
                        )

                
                self.cursor.execute("DELETE FROM Detalle_pedido WHERE id_pedido = %s", (id_pedido,))
                self.cursor.execute("DELETE FROM Pedido WHERE id_pedido = %s", (id_pedido,))

                self.conexion.commit()

                
                if self.pedido_seleccionado and int(self.pedido_seleccionado[0]) == id_pedido:
                    self.pedido_seleccionado = None

                self.cursor.execute("SELECT * FROM Pedido")
                self.pedidos_refresh = self.cursor.fetchall()
                self._refresh_table()

                self.mostrar_snack_bar("Pedido eliminado con éxito")
                confirm_dlg.open = False
                dlg.open = False
                self.page.update()
            except Exception as ex:
                self.conexion.rollback()
                print(f"Error al eliminar pedido: {ex}")
                self.mostrar_snack_bar("Error al eliminar el pedido")
                confirm_dlg.open = False
                self.page.update()
                
        def confirmar_eliminacion(e):
            confirm_dlg = ft.AlertDialog(
                modal=True,
                bgcolor="#fdd0b5",
                title=ft.Text("Confirmar eliminación", style=self.estilo_texto(), size=18),
                content=ft.Text(
                    "Vas a eliminar este pedido.\nSe devolverá al stock la materia prima utilizada.\n¿Deseas continuar?",
                    style=self.estilo_texto()
                ),
                actions=[
                    ft.TextButton(
                        "Cancelar",
                        style=self.estilo_de_botones(),
                        on_click=lambda ev: (setattr(confirm_dlg, "open", False), self.page.update())
                    ),
                    ft.TextButton(
                        "Eliminar",
                        style=self.estilo_de_botones(),
                        on_click=lambda ev: eliminar_pedido_confirmado(confirm_dlg)
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.overlay.append(confirm_dlg)
            confirm_dlg.open = True
            self.page.update()

        def guardar_cambios(e):
            if not tf_nombre.value.strip():
                self.mostrar_snack_bar("Ingresa un nombre de pedido")
                return
            if not tf_cliente.value.strip():
                self.mostrar_snack_bar("Ingresa un cliente")
                return
            fecha_val = fecha_label.value or str(datetime.today().date())


            nuevos = {}
            for it in estado["items"]:
                if it["cantidad"] < 0:
                    self.mostrar_snack_bar("Cantidades negativas no permitidas")
                    return
                if it["cantidad"] > 0:
                    nuevos[it["id"]] = float(it["cantidad"])

            originales = estado["original"]
            todos_ids = set(list(originales.keys()) + list(nuevos.keys()))
            deltas = {pid: nuevos.get(pid, 0.0) - originales.get(pid, 0.0) for pid in todos_ids}

            ok, faltantes = verificar_incrementos(deltas)
            if not ok:
                msg = "Faltan insumos:\n" + "\n".join([f"- {f['nombre']}: falta {f['faltante']:.2f}" for f in faltantes])
                self.mostrar_snack_bar(msg)
                return

            try:
                self.cursor.execute(
                    "UPDATE Pedido SET nombre_pedido=%s, estado_pedido=%s, cliente=%s, fecha_pedido=%s WHERE id_pedido=%s",
                    (tf_nombre.value.strip(), dd_estado.value, tf_cliente.value.strip(), fecha_val, id_pedido)
                )

                for pid in todos_ids:
                    delta = deltas[pid]
                    if pid in originales and pid in nuevos:
                        self.cursor.execute(
                            "UPDATE Detalle_pedido SET cantidad=%s WHERE id_pedido=%s AND id_producto=%s",
                            (nuevos[pid], id_pedido, pid)
                        )
                    elif pid in originales and pid not in nuevos:
                        self.cursor.execute(
                            "DELETE FROM Detalle_pedido WHERE id_pedido=%s AND id_producto=%s",
                            (id_pedido, pid)
                        )
                    elif pid not in originales and pid in nuevos:
                        self.cursor.execute(
                            "INSERT INTO Detalle_pedido (id_pedido, id_producto, cantidad) VALUES (%s, %s, %s)",
                            (id_pedido, pid, nuevos[pid])
                        )
                    ajustar_stock_por_delta(pid, delta)

                self.conexion.commit()
                self.cursor.execute("SELECT * FROM Pedido")
                self.pedidos_refresh = self.cursor.fetchall()
                self._refresh_table()
                self.mostrar_snack_bar("Pedido modificado con éxito")
                dlg.open = False
                self.page.update()
                
            except Exception as ex:
                self.conexion.rollback()
                print(f"Error al modificar pedido: {ex}")
                self.mostrar_snack_bar("Error al modificar el pedido")
                
        contenido_modificar = ft.Container(
            width=760,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("Modificar pedido", size=16, weight="bold", style=self.estilo_texto()),
                    ft.Row(
                        controls=[
                            tf_nombre,
                            tf_cliente,
                            dd_estado,
                            ft.TextButton("Fecha", style=self.estilo_de_botones(), on_click=lambda _: self.page.open(date_picker)),
                            fecha_label,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    ft.Text("Ítems del pedido", weight="bold", style=self.estilo_texto()),
                    lista_items,
                    ft.Row(
                        controls=[
                            dd_productos,
                            tf_cantidad_nueva,
                            ft.ElevatedButton("Agregar producto", style=self.estilo_de_botones(), on_click=agregar_item_nuevo),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                ],
            ),
        )

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor="#fdd0b5",
            title=ft.Text("Modificar pedido", style=self.estilo_texto(), size=25),
            content=contenido_modificar,
            actions=[
                ft.TextButton("Eliminar", style=self.estilo_de_botones(), on_click=confirmar_eliminacion),
                ft.TextButton("Cancelar", style=self.estilo_de_botones(), on_click=lambda e: (setattr(dlg, "open", False), self.page.update())),
                ft.TextButton("Guardar", style=self.estilo_de_botones(), on_click=guardar_cambios),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dlg)
        self.page.overlay.append(date_picker)
        dlg.open = True
        self.page.update()

    def armar_vista(self):
        
        self.cursor.execute("SELECT * FROM Pedido")
        pedidos = self.cursor.fetchall()
        self.pedidos_refresh = pedidos

        self._load_totales()

        header = ft.Row(
            controls=[
                ft.Container(ft.Text("Nombre pedido", weight="bold", style=self.estilo_texto()), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Cliente", weight="bold", style=self.estilo_texto()), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Fecha del pedido", weight="bold", style=self.estilo_texto()), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Precio total", weight="bold", style=self.estilo_texto()), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Estado del pedido", weight="bold", style=self.estilo_texto()), expand=True, padding=10, bgcolor="#ffc08d"),
            ],
            spacing=0
        )

        date_picker = ft.DatePicker(
            on_change=lambda e: self.filtrar_por_fecha(e.control.value),
            first_date=datetime(2023, 1, 1),
            last_date=datetime(2026, 12, 31),
        )


        filtro_grilla = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Filtrar por fecha:", style=self.estilo_texto(),size=15),
                    ft.TextButton(
                        "Seleccionar fecha",
                        style=self.estilo_de_botones(),
                        on_click=lambda _: self.page.open(date_picker),
                    ),
                    ft.TextButton("Limpiar filtro", style=self.estilo_de_botones(), on_click=lambda _: self.limpiar_filtro()),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            padding=10,
        )

        self.rows_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)
        self._refresh_table()
        

        grilla_pedidos = ft.Container(
            expand=True,
            bgcolor="#fdd0b5",
            content=ft.Column(
                [
                    header,
                    self.rows_container,
                ],
                expand=True,
            ),
            height=550,
            width=1100,
            border_radius=10,
            padding=0,
            border=ft.border.all(1, "#37373A"),
        )

        logo_pana = ft.Image(
            src=resource_path("Logo_panaderia_janssen.png"),
            width=100,             
            height=100,
            fit=ft.ImageFit.CONTAIN
        )

        boton_modificar_producto = ft.ElevatedButton(
            "Modificar Producto",
            width=100,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.mostrar_ventana_modificar_producto()
        )
        
        boton_cargar_materia_prima = ft.ElevatedButton(
            "Cargar Materia Prima",
            width=100,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.page.go("/vista_carga_mp")
        )
        
        boton_cargar_producto = ft.ElevatedButton(
            "Cargar Producto",
            width=100,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.page.go("/vista_cargar_producto")
        )
                
        boton_control_stock_mp = ft.ElevatedButton(
            "Consultar Materia Prima",
            width=100,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.page.go("/vista_controlar_stock")
        )
        
        barra_navegacion = ft.Container(
            border_radius=10,
            bgcolor="#fdd0b5",
            padding=10,
            height=600,
            width=145,
            expand=True,
            content=ft.Column(
                controls=[
                    logo_pana,
                    boton_cargar_materia_prima,
                    boton_control_stock_mp,
                    boton_cargar_producto,
                    boton_modificar_producto,
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
            border=ft.border.all(1, "#37373A"),
        )
        
        texto_principal = ft.Text(
            "Pedidos",
            size=30,
            style= self.estilo_texto()
        )       
        
        texto_modificar_pedido = ft.Text(
            "Modificar Pedidos",
            style=self.estilo_texto(),
            size=15
        )
        
        boton_modificar_pedido = ft.ElevatedButton(
            content=ft.Row(
                controls=[ft.Icon(name=ft.Icons.CREATE_OUTLINED)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=100,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.mostrar_ventana_modificar_pedido()
        )
        
        texto_cargar_pedido = ft.Text(
            "Cargar Pedidos",
            style=self.estilo_texto(),
            size=15,
        )        
        
        boton_cargar_pedido = ft.ElevatedButton(
            content=ft.Row(
                controls=[ft.Icon(name=ft.Icons.ADD_CIRCLE)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=100,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.mostrar_ventana_cargar_pedido()
        )
        
        titulo_row = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                texto_principal,
                ft.Row(
                    spacing=10,
                    controls=[filtro_grilla,texto_modificar_pedido, boton_modificar_pedido, texto_cargar_pedido, boton_cargar_pedido]
                )
            ]
        )

        self.page.add(
            ft.Row(
                expand=True,
                controls=[
                    ft.Column(
                        expand=False,
                        controls=[barra_navegacion],
                    ),
                    ft.Column(
                        expand=True,
                        controls=[titulo_row,grilla_pedidos],
                        
                    ),
                ]
            )
        )
