
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
from backend.controladores_pana.control_cargar_materia_prima import CargarMateriaPrima


class vista_carga_mp_nueva(configuracion_pantalla):

    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(""),
            open=False,
            duration=2000,
        )
        self.armar_vista()
    
    def mostrar_snack_bar(self, mensaje):
        self.page.open(ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#fdcb80",
            duration=3500
        ))
        self.page.update()


    
    def guardar_materia_prima(self, e):
        nombre = self.entry1.value.strip()
        distribuidor = self.entry2.value.strip()

        if not nombre or not distribuidor:
            self.mostrar_snack_bar("Completa ambos campos")
            return
        
        controlador = CargarMateriaPrima()
        try:
            resultado = controlador.cargar_materia_prima(nombre, distribuidor)
            if resultado:
                self.mostrar_snack_bar("Materia prima cargada con éxito")
                self.entry1.value = ""
                self.entry2.value = ""
                self.page.update()
            else:
                self.mostrar_snack_bar("Error al cargar materia prima")
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

        boton_eliminar_mp = ft.ElevatedButton(
            width=200,
            height=35,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT:"#37373A",
                    ft.ControlState.HOVERED:"#606065"},
                bgcolor={ft.ControlState.DEFAULT:"#a72d2d",
                        ft.ControlState.HOVERED:"#b84444"},
                shape={
                    "": ft.RoundedRectangleBorder(radius=4)
                },
                padding=15
            ),
            content=ft.Row(
                controls=[ft.Icon(name=ft.Icons.HIGHLIGHT_REMOVE_SHARP),
                          ft.Text("Eliminar Materia Prima")],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

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
                        ft.Row(
                            controls=[
                                texto_carga_mp,boton_eliminar_mp
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=105,
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