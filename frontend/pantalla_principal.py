from backend.conexion_a_BD.conexion_db import conectar
import flet as ft

class vista_principal:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.armar_vista()

    def config_page(self):
        self.page.controls.clear()
        self.page.title = "Pantalla Principal"
        self.page.bgcolor = "#ffebdf"
        self.page.scroll = ft.ScrollMode.AUTO
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()


    def armar_vista(self):
        
        self.cursor.execute("SELECT * FROM Pedido")
        pedidos = self.cursor.fetchall()

        filas = []
        for pedido in pedidos:
            filas.append(
                ft.DataRow(
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


        grilla_pedidos = ft.Container(
            expand=True,
            bgcolor="#fdd0b5",
            content=ft.Column(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Nombre pedido", style=ft.TextStyle(color="#37373A"))),
                            ft.DataColumn(ft.Text("Cantidad", style=ft.TextStyle(color="#37373A"))),
                            ft.DataColumn(ft.Text("Precio", style=ft.TextStyle(color="#37373A"))),
                            ft.DataColumn(ft.Text("Cliente", style=ft.TextStyle(color="#37373A"))),
                            ft.DataColumn(ft.Text("Fecha del pedido", style=ft.TextStyle(color="#37373A"))),
                            ft.DataColumn(ft.Text("Estado del pedido", style=ft.TextStyle(color="#37373A"))),
                        ],
                        rows=filas
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,  # Scroll en el Column
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
                        controls=[texto_principal,grilla_pedidos],
                    ),
                ]
            )
        )
