import flet as ft
from frontend.pantalla_login import PantallaLogin
from frontend.pantalla_principal import vista_principal

def main(page: ft.Page):
    
    page.window_fullscreen = True
    page.window_maximized = True
    page.window_resizable = False
    page.update()
    
    
    def cambiar_pantalla(e):
        if page.route == "/":
            PantallaLogin(page)
        elif page.route == "/vista_principal":
            vista_principal(page)
        page.update()

    page.on_route_change = cambiar_pantalla

    # Fuerza la ruta inicial a "/" y ejecuta la vista login
    page.go("/")



if __name__ == "__main__":
    ft.app(target=main)