
import flet as ft
from backend.conexion_a_BD.conexion_db import conectar
from frontend.pantalla_principal import vista_principal


class vista_carga_mp:

    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.armar_vista()

    def config_page(self):
        self.page.controls.clear()
        self.page.title = "Cargar Materia Prima"
        self.page.bgcolor = "#ffebdf"
        self.page.scroll = ft.ScrollMode.AUTO
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()



