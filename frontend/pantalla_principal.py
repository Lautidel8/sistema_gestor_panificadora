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
        self.page.bgcolor = "#040404"
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
                        ft.DataCell(ft.Text(str(pedido[1]))),
                        ft.DataCell(ft.Text(str(pedido[5]))),
                        ft.DataCell(ft.Text(str(pedido[3]))), 
                        ft.DataCell(ft.Text(str(pedido[4]))),
                        ft.DataCell(ft.Text(str(pedido[6]))),
                        ft.DataCell(ft.Text(str(pedido[2]))),
                    ]
                )
            )


    
        grilla_pedidos = ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Nombre pedido")),
                            ft.DataColumn(ft.Text("Cantidad")),
                            ft.DataColumn(ft.Text("Precio")),
                            ft.DataColumn(ft.Text("Cliente")),
                            ft.DataColumn(ft.Text("Fecha del pedido")),
                            ft.DataColumn(ft.Text("Estado del pedido")),
                        ],
                        rows=filas
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,  # Scroll en el Column
            ),
            height=600,
            border_radius=10,
            padding=10,
        )


        boton_superior = ft.Container(
            content=ft.ElevatedButton("Cargar nuevo pedido"),
            padding=10
        )

        self.page.add(
            ft.Row(
                expand=True,
                controls=[
                ft.Column(
                    controls=[
                        boton_superior,
                    ],
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        grilla_pedidos
                    ],
                )]
            )    
        )

                    # alignment=ft.MainAxisAlignment.CENTER,
                    # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    # spacing=30