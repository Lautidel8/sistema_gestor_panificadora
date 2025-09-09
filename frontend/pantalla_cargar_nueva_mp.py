
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla


class vista_carga_mp_nueva(configuracion_pantalla):

    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.armar_vista()
        
    def armar_vista(self):
        
        texto_carga_mp = ft.Text("Cargar Materia Prima Nueva", style=self.estilo_texto(),size=15)
        
        
        entry1 = ft.TextField(label="Nombre Materia Prima", width=300,label_style=ft.TextStyle(color="#37373A"),
                                border_color="#37373A", focused_border_color="#545454",text_style=ft.TextStyle(color="#37373A"))
        entry2 = ft.TextField(label="Distribuidor", width=300,label_style=ft.TextStyle(color="#37373A"),
                                border_color="#37373A", focused_border_color="#545454",text_style=ft.TextStyle(color="#37373A"))

        boton_guardar = ft.ElevatedButton("Guardar", width=100, style=self.estilo_de_botones())

        container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    entry1,
                    ft.Container(height=10),
                    entry2,
                    ft.Container(height=10),
                    boton_guardar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=ft.padding.all(20),
            width=500,
            height=400,
            bgcolor="#fdd0b5",
            border_radius=10,
            border=ft.border.all(2, "#37373A"),
        )
        
        self.page.add(
            ft.Container(
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Row(
                            controls=[
                                texto_carga_mp
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=130,
                        ),
                        container_principal
                    ]
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=110),
                expand=True,
            )
        )