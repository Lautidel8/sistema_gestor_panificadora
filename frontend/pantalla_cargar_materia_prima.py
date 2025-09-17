
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
from backend.controladores_pana.control_cargar_materia_prima import CargarMateriaPrima


class vista_carga_mp(configuracion_pantalla):

    def __init__(self, page: ft.Page):
        self.page = page
        self.resultados = ft.Column(scroll="auto", height=80, spacing=0)
        self.materias_primas = []
        self.busqueda = None 
        self.config_page()
        self.armar_vista()
        
    def dropdown_materia_prima(self):
        controlador = CargarMateriaPrima()
        try:
            materias_primas = controlador.listar_materias_primas()
        finally:
            controlador.cerrar_conexion()


        self.materias_primas = materias_primas

        self.busqueda = ft.TextField(
            label="Buscar Materia Prima",
            width=300,
            on_change=self.filtrar_opciones,  # filtra en cada tecla
            border_color="#37373A",
            focused_border_color="#545454",
            text_style=self.estilo_texto()
        )

        self.resultados.controls.clear()

        return ft.Column([self.busqueda, self.resultados])

    def filtrar_opciones(self, e):
        texto = e.control.value.lower()
        self.resultados.controls.clear()

        for mp in self.materias_primas:
            if texto in mp.lower():
                self.resultados.controls.append(
                    ft.Container(
                        bgcolor="#f8c499",
                        border_radius=5,
                        content=ft.ListTile(
                            title=ft.Text(mp, style=self.estilo_texto()),
                            on_click=lambda ev, valor=mp: self.seleccionar_opcion(valor)
                        ),
                    )
                )
        e.page.update()

    def seleccionar_opcion(self, valor):
        self.busqueda.value = valor
        self.resultados.controls.clear()
        self.busqueda.page.update()


    def armar_vista(self):
        
        texto_carga_mp = ft.Text("Cargar Materia Prima", style=self.estilo_texto(),size=15)
        
        boton_cargar_mp_nueva = ft.ElevatedButton(
            "Cargar Nueva Materia Prima",
            style=self.estilo_de_botones(),
            width=220,
            on_click=lambda e: self.page.go("/vista_carga_mp_nueva")
        )

        materia_prima_dropdown = self.dropdown_materia_prima()
        entry1 = ft.TextField(label="Cantidad",focused_border_color="#545454", width=300,label_style=self.estilo_texto())

        boton_guardar = ft.ElevatedButton("Guardar", width=100, style=self.estilo_de_botones())

        container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    materia_prima_dropdown,
                    ft.Container(height=10),
                    entry1,
                    ft.Container(height=10),
                    boton_guardar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=ft.padding.all(20),
            width=500,
            height=400,
            bgcolor="#fdd0b5",
            border_radius=10,
            border=ft.border.all(2, "#37373A"),
        )


        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[self.boton_volver()],
                            alignment=ft.MainAxisAlignment.START,
                            expand=True
                        ),
                        ft.Container(height=40),
                        ft.Row(
                            controls=[
                                texto_carga_mp,boton_cargar_mp_nueva
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=130,
                        ),
                        container_principal
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        )

