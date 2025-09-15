
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