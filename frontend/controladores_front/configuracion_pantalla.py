
from backend.conexion_a_BD.conexion_db import conectar
import flet as ft

class configuracion_pantalla:
    
    def config_page(self):
        self.page.controls.clear()
        self.page.title = "Sistema Panaderia Janssen"
        self.page.bgcolor = "#ffebdf"
        self.page.scroll = ft.ScrollMode.AUTO
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()
        
    def estilo_texto(self):
        return ft.TextStyle(
            color="#37373A",
            font_family="Arial",
        )

    def estilo_de_botones(self):
        return ft.ButtonStyle(
            text_style=ft.TextStyle(
                font_family="Arial",
            ),
            color={ft.ControlState.DEFAULT:"#fdd0b5",
                     ft.ControlState.HOVERED:"#37373A"},
            bgcolor={ft.ControlState.DEFAULT:"#37373A",
                     ft.ControlState.HOVERED:"#ffc08d",},
            shape={
                "": ft.RoundedRectangleBorder(radius=4)
                
            },
            padding=15
        )

    def boton_volver(self):
        boton_volver = ft.ElevatedButton(
            content=ft.Row(
                controls=[ft.Icon(name=ft.Icons.HOME)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=50,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.page.go("/vista_principal")
        )
        return boton_volver
    
    
    def mostrar_snack_bar(self, mensaje):
        self.page.open(ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="#fdcb80",
            duration=3500
        ))
        self.page.update()

    def crear_dialogo_selector(self, titulo, opciones, texto_accion, on_accion, color_dialogo="#fdd0b5"):
        seleccion = {"valor": None}
        radio_group = ft.RadioGroup(
            content=ft.ListView(
                controls=[
                    ft.Radio(
                        value=opcion,
                        label=opcion,
                        label_style=ft.TextStyle(
                            color="#37373A",
                            font_family="Arial",
                            size=15
                        )
                    ) for opcion in opciones
                ],
                spacing=10,
                padding=10,
                height=300,
                width=300,
            ),
            on_change=lambda e: seleccion.update({"valor": e.control.value})
        )
        
        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo, style=self.estilo_texto(), size=15),
            content=ft.Container(
                content=ft.Column(
                    controls=[radio_group],
                    scroll="auto",
                    height=300,
                ),
                width=300,
                bgcolor=color_dialogo,
                border_radius=10,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar", 
                    style=self.estilo_de_botones(), 
                    on_click=lambda e: self.cerrar_dialogo(dialogo)
                ),
                ft.TextButton(
                    texto_accion, 
                    style=self.estilo_de_botones(),
                    on_click=lambda e: on_accion(e, dialogo, seleccion["valor"])
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        return dialogo, seleccion
    

    def mostrar_dialogo(self, dialogo):
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()

    def cerrar_dialogo(self, dialogo):
        dialogo.open = False
        self.page.update()

