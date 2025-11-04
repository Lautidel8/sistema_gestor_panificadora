import flet as ft
import sys
import os
from backend.util_paths import resource_path
from frontend.pantalla_login import PantallaLogin
from frontend.pantalla_principal import vista_principal
from frontend.pantalla_cargar_materia_prima import vista_carga_mp
from frontend.pantalla_cargar_nueva_mp import vista_carga_mp_nueva
from frontend.pantalla_controlar_stock import vista_controlar_stock
from frontend.pantalla_cargar_producto import vista_cargar_producto


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
            
        elif page.route == "/vista_controlar_stock":
            vista_controlar_stock(page)
            
        elif page.route == "/vista_cargar_producto":
            vista_cargar_producto(page)

        page.update()

    page.on_route_change = cambiar_pantalla

    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)