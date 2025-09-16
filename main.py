import flet as ft
from frontend.pantalla_login import PantallaLogin
from frontend.pantalla_principal import vista_principal
from frontend.pantalla_cargar_materia_prima import vista_carga_mp
from frontend.pantalla_cargar_nueva_mp import vista_carga_mp_nueva

def main(page: ft.Page):
    
    page.window_fullscreen = True
    page.window_resizable = False
    
    
    def cambiar_pantalla(e):
        if page.route == "/":
            PantallaLogin(page)
            
        elif page.route == "/vista_principal":
            vista_principal(page)
            
        elif page.route == "/vista_carga_mp":
            vista_carga_mp(page)
        
        elif page.route == "/vista_carga_mp_nueva":
            vista_carga_mp_nueva(page)
            
        page.update()

    page.on_route_change = cambiar_pantalla

    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)