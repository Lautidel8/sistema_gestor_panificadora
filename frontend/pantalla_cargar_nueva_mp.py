
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
from backend.controladores_pana.control_cargar_materia_prima import CargarMateriaPrima


class vista_carga_mp_nueva(configuracion_pantalla):

    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.armar_vista()
        
    def guardar_materia_prima(self, e):
        nombre = self.entry1.value.strip()
        distribuidor = self.entry2.value.strip()
        if not nombre or not distribuidor:
            self.page.snack_bar = ft.SnackBar(ft.Text("Completa ambos campos"), open=True)
            self.page.update()
            return
        
        controlador = CargarMateriaPrima()
        try:
            resultado = controlador.cargar_materia_prima(nombre, distribuidor)
            if resultado:
                self.page.snack_bar = ft.SnackBar(ft.Text("Materia prima cargada con éxito"), open=True)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Error al cargar materia prima"), open=True)
            self.page.update()
        finally:
            controlador.cerrar_conexion()

    def armar_vista(self):
        
        texto_carga_mp = ft.Text("Cargar Materia Prima Nueva", style=self.estilo_texto(),size=15)

        self.entry1 = ft.TextField(label="Nombre Materia Prima", width=300,label_style=ft.TextStyle(color="#37373A"),
                                border_color="#37373A", focused_border_color="#545454",text_style=ft.TextStyle(color="#37373A"))
        self.entry2 = ft.TextField(label="Distribuidor", width=300,label_style=ft.TextStyle(color="#37373A"),
                                border_color="#37373A", focused_border_color="#545454",text_style=ft.TextStyle(color="#37373A"))

        boton_guardar = ft.ElevatedButton("Guardar", width=100, style=self.estilo_de_botones(),
                                          on_click=self.guardar_materia_prima)


        container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    self.entry1,
                    ft.Container(height=10),
                    self.entry2,
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
                        texto_carga_mp,
                        container_principal
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        )