import flet as ft

def main(page: ft.Page):
    # Configuración de ventana antes de mostrar la UI
    page.window_fullscreen = True
    page.window_resizable = False

    # Controles de ejemplo
    page.add(ft.Text("La app inicia en fullscreen"))

ft.app(target=main)
