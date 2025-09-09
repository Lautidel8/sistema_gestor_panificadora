
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
import flet as ft
from datetime import datetime

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
            
        # Convertir fecha del DatePicker a formato adecuado
        fecha_str = fecha.strftime('%Y-%m-%d')
        
        if not hasattr(self, 'pedidos_originales'):
            self.pedidos_originales = self.pedidos_refresh.copy()

        self.pedidos_refresh = [p for p in self.pedidos_originales if str(p[4]) == fecha_str]

        self._refresh_table()
        self.page.update()
        
        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Mostrando pedidos del {fecha_str}"),
            open=True
        )

    def limpiar_filtro(self):
        """Limpia el filtro y muestra todos los pedidos"""
        if hasattr(self, 'pedidos_originales'):
            self.pedidos_refresh = self.pedidos_originales.copy()
            self._refresh_table()
            self.page.update()
            
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Filtro limpiado"),
                open=True
            )



    def armar_vista(self):
        
        
        self.cursor.execute("SELECT * FROM Pedido")
        pedidos = self.cursor.fetchall()
        self.pedidos_refresh = pedidos    #guardo pedidos para refrescar

        # cargar totales iniciales
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
        )

        logo_pana = ft.Image(
            src="logo_panaderia.png",
            width=100,             
            height=100,
            fit=ft.ImageFit.CONTAIN
        )

        boton_generar_reporte = ft.ElevatedButton(
            "Generar Reporte",
            width=100,
            style=self.estilo_de_botones()
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
            style=self.estilo_de_botones()
        )
                
        boton_control_stock_mp = ft.ElevatedButton(
            "Consultar Materia Prima",
            width=100,
            style=self.estilo_de_botones()
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
                    boton_generar_reporte,                   
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
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
            style=self.estilo_de_botones()
        )
        
        texto_cargar_pedido = ft.Text(
            "Cargar Pedidos",
            style=self.estilo_texto(),
            size=15
        )        
        
        boton_cargar_pedido = ft.ElevatedButton(
            content=ft.Row(
                controls=[ft.Icon(name=ft.Icons.ADD_CIRCLE)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=100,
            style=self.estilo_de_botones()
        )
        
        titulo_row = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,   # título a la izquierda, botones a la derecha
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # centra verticalmente título y botones
            controls=[
                texto_principal,
                ft.Row(                                      # fila interna para separar botones
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
