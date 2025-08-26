from backend.conexion_a_BD.conexion_db import conectar
import flet as ft

class vista_principal:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.pedido_seleccionado = None
        self.pedido_guardado = None
        self.pedidos_refresh = []    # lista de pedidos para refrescar }
        self.data_table = None    # referencia al DataTable para actualizar filas
        self.totales_map = {}
        self.rows_container = None
        self.config_page()
        self.armar_vista()

    def config_page(self):
        self.page.controls.clear()
        self.page.title = "Pantalla Principal"
        self.page.bgcolor = "#ffebdf"
        self.page.scroll = ft.ScrollMode.AUTO
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()

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
        
        # recargar totales por si cambiaron los detalles
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
                            ft.Container(ft.Text(str(pedido[1]), style=ft.TextStyle(color="#37373A")), expand=True, padding=10),
                            ft.Container(ft.Text(str(pedido[3]), style=ft.TextStyle(color="#37373A")), expand=True, padding=10),
                            ft.Container(ft.Text(str(pedido[4]), style=ft.TextStyle(color="#37373A")), expand=True, padding=10),
                            ft.Container(ft.Text(total_display, style=ft.TextStyle(color="#37373A")), expand=True, padding=10),
                            ft.Container(ft.Text(str(pedido[2]), style=ft.TextStyle(color="#37373A")), expand=True, padding=10),
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
        # no olvidar actualizar la página desde quien lo llame (aquí sí lo hacemos)
        self.page.update()

    def armar_vista(self):
        
        self.cursor.execute("SELECT * FROM Pedido")
        pedidos = self.cursor.fetchall()
        self.pedidos_refresh = pedidos    #guardo pedidos para refrescar

        # cargar totales iniciales
        self._load_totales()

        header = ft.Row(
            controls=[
                ft.Container(ft.Text("Nombre pedido", weight="bold", style=ft.TextStyle(color="#37373A")), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Cliente", weight="bold", style=ft.TextStyle(color="#37373A")), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Fecha del pedido", weight="bold", style=ft.TextStyle(color="#37373A")), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Precio total", weight="bold", style=ft.TextStyle(color="#37373A")), expand=True, padding=10, bgcolor="#ffc08d"),
                ft.Container(ft.Text("Estado del pedido", weight="bold", style=ft.TextStyle(color="#37373A")), expand=True, padding=10, bgcolor="#ffc08d"),
            ],
            spacing=0
        )

        # Contenedor scrollable solo con las filas
        self.rows_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)

        # primer llenado de filas
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
        )

        barra_navegacion = ft.Container(
            border_radius=10,
            bgcolor="#fdd0b5",
            padding=10,
            height=600,
            width=120,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Icon("home"),
                    ft.Icon("location_on"),
                    ft.Icon("calendar_month"),
                    ft.Icon("settings"),
                    ft.Icon("power_settings_new"),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
        )
        
        texto_principal = ft.Text(
            "Pedidos",
            color="#37373A",
            size=30
        )
        
        boton_controlar_stock = ft.ElevatedButton(
            "x",
            #on_click=self.validar_ingreso,
            color="#fdd0b5",
            bgcolor="#37373A",
            width=100,
        )
        
        
        texto_modificar_pedido = ft.Text(
            "Modificar Pedidos",
            color="#37373A",
            size=15
        )
        
        boton_modificar_pedido = ft.ElevatedButton(
            "x",
            #on_click=self.validar_ingreso,
            color="#fdd0b5",
            bgcolor="#37373A",
            width=100,
        )
        
        texto_cargar_pedido = ft.Text(
            "Cargar Pedidos",
            color="#37373A",
            size=15
        )        
        
        boton_cargar_pedido = ft.ElevatedButton(
            "y",
            #on_click=self.validar_ingreso,
            color="#fdd0b5",
            bgcolor="#37373A",
            width=100,
        )
        
        titulo_row = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,   # título a la izquierda, botones a la derecha
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # centra verticalmente título y botones
            controls=[
                texto_principal,
                ft.Row(                                      # fila interna para separar botones
                    spacing=10,
                    controls=[texto_modificar_pedido, boton_modificar_pedido, texto_cargar_pedido, boton_cargar_pedido]
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
