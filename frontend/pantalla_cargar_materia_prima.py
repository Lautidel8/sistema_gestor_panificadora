
import flet as ft
from backend.conexion_a_BD.conexion_db import conectar


def main(page: ft.Page):
    page.add(ft.Text("Pantalla Cargar Materia Prima"))
    
    
    

if __name__ == "__main__":
    ft.app(target=main)