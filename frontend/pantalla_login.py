
from backend.controladores_pana.control_Contrasenia import Valida_contrasenia
import flet as ft


class PantallaLogin:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.armar_vista()

    def config_page(self):
        self.page.controls.clear()
        self.page.title = "Sistema Panadería Janssen"
        self.page.bgcolor = "#ffebdf"

    def validar_ingreso(self, e):
        resultado = Valida_contrasenia.verficar_contra(self.contra.value)
        if resultado:
            self.page.go("/vista_principal")
        else:
            print("Contraseña incorrecta")
        self.page.update()

    def armar_vista(self):
        texto_titulo = ft.Text(
            "Sistema de Panadería Janssen",
            color="#fdd0b5",
            size=80
        )
        texto1 = ft.Text(
            "Ingrese la contraseña para continuar:",
            color="#37373A",
            size=15
        )

        self.contra = ft.TextField(
            label="Contraseña",
            can_reveal_password=True,
            password=True,
            border_color="#fdd0b5",
            focused_border_color="#fdd0b5",
            label_style=ft.TextStyle(color="#37373A"),
            text_style=ft.TextStyle(color="#37373A"),
            width=400
        )

        boton_ingresar = ft.ElevatedButton(
            "Ingresar",
            on_click=self.validar_ingreso,
            color="#fdd0b5",
            bgcolor="#37373A",
            width=200,
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        texto_titulo,
                        texto1,
                        self.contra,
                        boton_ingresar
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        )




