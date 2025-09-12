
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla


class vista_carga_mp(configuracion_pantalla):

    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.armar_vista()


    def armar_vista(self):
        
        texto_carga_mp = ft.Text("Cargar Materia Prima", style=self.estilo_texto(),size=15)
        
        boton_cargar_mp_nueva = ft.ElevatedButton(
            "Cargar Nueva Materia Prima",
            style=self.estilo_de_botones(),
            width=220,
            on_click=lambda e: self.page.go("/vista_carga_mp_nueva")
        )
        
        entry1 = ft.TextField(label="Materia Prima", width=300,label_style=ft.TextStyle(color="#37373A"),
                                border_color="#37373A", focused_border_color="#545454",text_style=ft.TextStyle(color="#37373A"))
        entry2 = ft.TextField(label="Cantidad", width=300,label_style=ft.TextStyle(color="#37373A"),
                                border_color="#37373A", focused_border_color="#545454",text_style=ft.TextStyle(color="#37373A"))
        entry3 = ft.TextField(label="Unidad", width=300,label_style=ft.TextStyle(color="#37373A"),
                                border_color="#37373A", focused_border_color="#545454",text_style=ft.TextStyle(color="#37373A"))


        boton_guardar = ft.ElevatedButton("Guardar", width=100, style=self.estilo_de_botones())

        container_principal = ft.Container(
            content=ft.Column(
                controls=[


                    entry1,
                    ft.Container(height=10),
                    entry2,
                    ft.Container(height=10),
                    entry3,
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
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[self.boton_volver()],
                            alignment=ft.MainAxisAlignment.START,
                            expand=True
                        ),
                        ft.Container(height=40),
                        ft.Row(
                            controls=[
                                texto_carga_mp,boton_cargar_mp_nueva
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=130,
                        ),
                        container_principal
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        )

