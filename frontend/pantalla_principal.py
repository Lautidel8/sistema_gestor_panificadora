from backend.conexion_a_BD.conexion_db import conectar
import flet as ft

class vista_principal:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.pedido_seleccionado = None
        self.pedido_guardado = None
        self.pedidos_refresh = []    # { changed code: lista de pedidos para refrescar }
        self.data_table = None    # { changed code: referencia al DataTable para actualizar filas
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
        if hasattr(e, "data") and not e.data:
            self.pedido_seleccionado = None
        else:
            self.pedido_seleccionado = pedido
        self._refresh_table()
        self.page.update()        
        
    def _refresh_table(self):
        if not self.data_table:
            return
        
        
        

    def armar_vista(self):
        
        self.cursor.execute("SELECT * FROM Pedido")
        pedidos = self.cursor.fetchall()
        self.pedidos_refresh = pedidos    #guardo pedidos para refrescar

        filas = []
        for pedido in pedidos:
            filas.append(
                ft.DataRow(
                    selected=(self.pedido_seleccionado is not None and self.pedido_seleccionado[0] == pedido[0]),
                    on_select_changed=lambda e, pedido=pedido: self.seleccionar_pedido(e, pedido),
                    cells=[
                        ft.DataCell(ft.Text(str(pedido[1]), style=ft.TextStyle(color="#37373A"))),
                        ft.DataCell(ft.Text(str(pedido[5]), style=ft.TextStyle(color="#37373A"))),
                        ft.DataCell(ft.Text(str(pedido[3]), style=ft.TextStyle(color="#37373A"))),
                        ft.DataCell(ft.Text(str(pedido[4]), style=ft.TextStyle(color="#37373A"))),
                        ft.DataCell(ft.Text(str(pedido[6]), style=ft.TextStyle(color="#37373A"))),
                        ft.DataCell(ft.Text(str(pedido[2]), style=ft.TextStyle(color="#37373A"))),
                        
                    ]
                )
            )

        self.data_table = ft.DataTable(               # { changed code: guardo la DataTable }
            columns=[
                ft.DataColumn(ft.Text("Nombre pedido", style=ft.TextStyle(color="#37373A"))),
                ft.DataColumn(ft.Text("Cantidad", style=ft.TextStyle(color="#37373A"))),
                ft.DataColumn(ft.Text("Precio", style=ft.TextStyle(color="#37373A"))),
                ft.DataColumn(ft.Text("Cliente", style=ft.TextStyle(color="#37373A"))),
                ft.DataColumn(ft.Text("Fecha del pedido", style=ft.TextStyle(color="#37373A"))),
                ft.DataColumn(ft.Text("Estado del pedido", style=ft.TextStyle(color="#37373A"))),
            ],
            rows=filas,
        )

        grilla_pedidos = ft.Container(
            expand=True,
            bgcolor="#fdd0b5",
            content=ft.Column(
                [
                    self.data_table,  
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
            height=550,
            width=1100,
            border_radius=10,
            padding=10,
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
        
        boton_modificar_pedido = ft.ElevatedButton(
            "x",
            #on_click=self.validar_ingreso,
            color="#fdd0b5",
            bgcolor="#37373A",
            width=100,
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
                    controls=[boton_modificar_pedido, boton_cargar_pedido]
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
