
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
from backend.controladores_pana.control_cargar_materia_prima import CargarMateriaPrima


class vista_carga_mp(configuracion_pantalla):

    def __init__(self, page: ft.Page):
        self.page = page
        self.resultados = ft.Column(scroll="auto", height=80, spacing=0)
        self.materias_primas = []
        self.busqueda = None
        self.materia_prima_seleccionada = None
        self.entry_cantidad = None
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
            on_change=self.filtrar_opciones,
            border_color="#37373A",
            label_style=self.estilo_texto(),
            focused_border_color="#545454",
            text_style=self.estilo_texto()
        )

        self.resultados.controls.clear()
        return ft.Column([self.busqueda, self.resultados])

    def seleccionar_opcion(self, valor, id_mp=None, unidad=None):
        self.busqueda.value = valor
        self.materia_prima_seleccionada = id_mp
        self.unidad_seleccionada = unidad
        self.resultados.controls.clear()
        
        if hasattr(self, 'entry_cantidad') and self.entry_cantidad:
            self.entry_cantidad.label = f"Cantidad ({unidad})"
            
        self.busqueda.page.update()

    def filtrar_opciones(self, e):
        texto = e.control.value.lower()
        self.resultados.controls.clear()

        for item in self.materias_primas:
            if isinstance(item, int) or isinstance(item, str):
                id_mp = item
                nombre_mp = str(item)
                unidad = ""  # No hay unidad disponible
            else:
                id_mp = item[0]
                nombre_mp = item[1]
                
                # Obtener la unidad (puede ser directamente de la consulta o necesitas buscarla)
                unidad = ""
                if len(item) >= 4:  # Si hay al menos 4 elementos en la tupla
                    # El último elemento es el nombre de la unidad
                    unidad = item[3] if item[3] else ""
                    
            if texto in str(nombre_mp).lower():
                self.resultados.controls.append(
                    ft.Container(
                        bgcolor="#f8c499",
                        border_radius=5,
                        border=ft.border.all(1, "#37373A"),
                        content=ft.ListTile(
                            title=ft.Text(str(nombre_mp), style=self.estilo_texto()),
                            subtitle=ft.Text(f"Unidad: {unidad}" if unidad else "", 
                                            style=self.estilo_texto(), 
                                            size=12),
                            on_click=lambda ev, valor=nombre_mp, id=id_mp, u=unidad: 
                                    self.seleccionar_opcion(valor, id, u)
                        ),
                    )
                )
        e.page.update()
        
    def guardar_cantidad_materia_prima(self, e):
        if not self.materia_prima_seleccionada:
            self.mostrar_snack_bar("Selecciona una materia prima")
            return
            
        cantidad_texto = self.entry_cantidad.value.strip()
        if not cantidad_texto:
            self.mostrar_snack_bar("Ingresa una cantidad")
            return
        
        try:
            cantidad = float(cantidad_texto)
        except ValueError:
            self.mostrar_snack_bar("La cantidad debe ser un número")
            return
            
        controlador = CargarMateriaPrima()
        try:
            resultado = controlador.actualizar_stock_materia_prima(
                self.materia_prima_seleccionada,
                cantidad
            )
            
            if resultado:
                self.mostrar_snack_bar(f"Cantidad actualizada correctamente")
                self.busqueda.value = ""
                self.entry_cantidad.value = ""
                self.materia_prima_seleccionada = None
                self.resultados.controls.clear()
                self.page.update()
            else:
                self.mostrar_snack_bar("Error al actualizar la cantidad")
        finally:
            controlador.cerrar_conexion()


    def armar_vista(self):
        
        texto_carga_mp = ft.Text("Cargar Materia Prima", style=self.estilo_texto(),size=15)
        
        boton_cargar_mp_nueva = ft.ElevatedButton(
            "Cargar Nueva Materia Prima",
            style=self.estilo_de_botones(),
            width=220,
            on_click=lambda e: self.page.go("/vista_carga_mp_nueva")
        )

        materia_prima_dropdown = self.dropdown_materia_prima()
        
        self.entry_cantidad = ft.TextField(
            label="Cantidad",
            focused_border_color="#545454", 
            width=300,
            label_style=self.estilo_texto(),
            text_style=self.estilo_texto()
        )
        

        boton_guardar = ft.ElevatedButton("Guardar", width=100, style=self.estilo_de_botones(),on_click=self.guardar_cantidad_materia_prima)

        container_principal = ft.Container(
            content=ft.Column(
                controls=[
                    materia_prima_dropdown,
                    ft.Container(height=10),
                    self.entry_cantidad,
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

