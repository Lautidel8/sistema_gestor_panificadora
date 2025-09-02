
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