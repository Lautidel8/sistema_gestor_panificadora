import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
from backend.controladores_pana.control_cargar_materia_prima import CargarMateriaPrima


class vista_carga_mp_nueva(configuracion_pantalla):

    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(""),
            open=False,
            duration=2000,
        )
        self.armar_vista()
    

    def guardar_materia_prima(self, e):
        nombre = self.entry1.value.strip()
        distribuidor = self.entry2.value.strip()
        id_unidad = self.dropdown_unidades.value

        if not nombre or not distribuidor or not id_unidad:
            self.mostrar_snack_bar("Completa todos los campos")
            return
        
        controlador = CargarMateriaPrima()
        try:
            resultado = controlador.cargar_materia_prima(nombre, distribuidor, id_unidad)
            if resultado:
                self.mostrar_snack_bar("Materia prima cargada con éxito")
                self.entry1.value = ""
                self.entry2.value = ""
                self.dropdown_unidades.value = None
                self.page.update()
            else:
                self.mostrar_snack_bar("Error al cargar materia prima")
        finally:
            controlador.cerrar_conexion()

    def mostrar_lista_materias_primas(self, e):
        controlador = CargarMateriaPrima()
        try:
            materias_primas = controlador.listar_materias_primas()
        finally:
            controlador.cerrar_conexion()

        if not materias_primas:
            self.mostrar_snack_bar("No hay materias primas registradas.")
            return

        seleccion = {"nombre": None}

        radio_group = ft.RadioGroup(
            content=ft.ListView(
                controls=[
                            ft.Radio(
                                # Usamos el nombre como value en lugar del ID
                                value=mp[1],
                                active_color="#454444",
                                label=f"{mp[1]}",
                                label_style=self.estilo_texto()
                            )
                            for mp in materias_primas
                        ],
                expand=True,
                spacing=5,
                auto_scroll=False,
            ),
            on_change=lambda e: seleccion.update({"nombre": e.control.value}),
        )

        ventana_eliminar_mp = ft.AlertDialog(
            modal=True,
            bgcolor="#a72d2d",
            title=ft.Text("Selecciona la materia prima a eliminar",style=self.estilo_texto(), size=15),
                content=ft.Container(
                    content=ft.Column(
                        controls=[radio_group],
                        scroll="auto",
                        height=300,
                    ),
                    width=300,
                    
                ),
            actions=[
                ft.TextButton("Cancelar",style=self.estilo_de_botones(), on_click=lambda e: self.cerrar_dialogo(ventana_eliminar_mp)),
                ft.TextButton(
                    "Eliminar",
                    style=self.estilo_de_botones(),
                    on_click=lambda e: self.eliminar_materia_prima_seleccionada(ventana_eliminar_mp, seleccion["nombre"])
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.clear()
        self.page.overlay.append(ventana_eliminar_mp)
        ventana_eliminar_mp.open = True
        self.page.update()


    def cerrar_dialogo(self, dialogo):
        dialogo.open = False
        self.page.update()


    def eliminar_materia_prima_seleccionada(self, dialogo, nombre):
        if not nombre:
            self.mostrar_snack_bar("Selecciona una materia prima.")
            return
        controlador = CargarMateriaPrima()
        try:
            resultado = controlador.eliminar_materia_prima(nombre)
            if resultado == True:
                self.mostrar_snack_bar("Materia prima eliminada.")
            elif resultado == "producto_asociado":
                self.mostrar_snack_bar("No se puede eliminar la materia prima ya que está asignada a un producto")
            else:
                self.mostrar_snack_bar("Error al eliminar materia prima.")
        finally:
            controlador.cerrar_conexion()
        dialogo.open = False
        self.page.update()


    def armar_vista(self):
        
        controlador = CargarMateriaPrima()
        try:
            unidades = controlador.listar_unidades()
        finally:
            controlador.cerrar_conexion()
        
        opciones_unidades = [
            ft.dropdown.Option(text=nombre, key=str(id_unidad))
            for id_unidad, nombre in unidades
        ]
        
        texto_carga_mp = ft.Text("Cargar Materia Prima Nueva", style=self.estilo_texto(), size=15)

        self.entry1 = ft.TextField(
            label="Nombre Materia Prima",
            width=300,
            label_style=ft.TextStyle(color="#37373A"),
            border_color="#37373A",
            focused_border_color="#545454",
            text_style=ft.TextStyle(color="#37373A")
        )
        self.entry2 = ft.TextField(
            label="Distribuidor",
            width=300,
            label_style=ft.TextStyle(color="#37373A"),
            border_color="#37373A",
            focused_border_color="#545454",
            text_style=ft.TextStyle(color="#37373A")
        )

        self.dropdown_unidades = ft.Dropdown(
            label="Unidad de medida",
            width=300,
            options=opciones_unidades,
            label_style=self.estilo_texto(),
            text_style=self.estilo_texto()
        )

        boton_guardar = ft.ElevatedButton(
            "Guardar",
            width=100,
            style=self.estilo_de_botones(),
            on_click=self.guardar_materia_prima
        )

        boton_eliminar_mp = ft.ElevatedButton(
            width=200,
            height=35,
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: "#37373A", ft.ControlState.HOVERED: "#606065"},
                bgcolor={ft.ControlState.DEFAULT: "#a72d2d", ft.ControlState.HOVERED: "#b84444"},
                shape={"": ft.RoundedRectangleBorder(radius=4)},
                padding=15
            ),
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.HIGHLIGHT_REMOVE_SHARP),
                    ft.Text("Eliminar Materia Prima")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=self.mostrar_lista_materias_primas
        )

        container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    self.entry1,
                    ft.Container(height=10),
                    self.entry2,
                    ft.Container(height=10),
                    self.dropdown_unidades,
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
                            controls=[texto_carga_mp, boton_eliminar_mp],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=105,
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
