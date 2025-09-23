
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla
from backend.controladores_pana.control_cargar_producto import control_cargar_producto

class vista_cargar_producto(configuracion_pantalla):
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.resultados = ft.Column(scroll="auto", height=80, spacing=0)
        self.materias_primas = []
        self.busqueda = None
        self.materias_primas_seleccionadas = []  # Lista para almacenar todas las MP seleccionadas
        self.config_page()
        self.cargar_materias_primas() 
        self.armar_vista()
    
    def cargar_materias_primas(self):
        from backend.controladores_pana.control_cargar_materia_prima import CargarMateriaPrima
        controlador = CargarMateriaPrima()
        try:
            self.materias_primas = controlador.listar_materias_primas()
        except Exception as e:
            print("Error al cargar materias primas:", e)
        finally:
            controlador.cerrar_conexion()
    
    def filtrar_opciones(self, e):

        texto = e.control.value.lower()
        self.resultados.controls.clear()
        
        
        for mp in self.materias_primas:

            if len(mp) >= 2:
                id_mp = mp[0]
                nombre_mp = mp[1]
                
                if texto and texto in nombre_mp.lower():
                    self.resultados.controls.append(
                        ft.Container(
                            bgcolor="#f8c499",
                            border_radius=5,
                            border=ft.border.all(1, "#37373A"),
                            content=ft.ListTile(
                                title=ft.Text(nombre_mp, style=self.estilo_texto()),
                                on_click=lambda ev, valor=nombre_mp, id=id_mp: self.seleccionar_opcion(valor, id)
                            ),
                        )
                    )
        e.page.update()
    
    def seleccionar_opcion(self, valor, id_mp):
        self.busqueda.value = valor
        self.materia_prima_seleccionada = {"id": id_mp, "nombre": valor, "cantidad": None}
        self.resultados.controls.clear()
        self.busqueda.page.update()
    
    def agregar_materia_prima(self, e):
        if not hasattr(self, 'materia_prima_seleccionada') or not self.materia_prima_seleccionada:
            self.mostrar_snack_bar("Selecciona una materia prima primero")
            return
        
        cantidad_texto = self.entry_cantidad.value.strip() if hasattr(self, 'entry_cantidad') and self.entry_cantidad.value else ""
        if not cantidad_texto:
            self.mostrar_snack_bar("Ingresa una cantidad")
            return
        
        try:
            cantidad = float(cantidad_texto)
            
            self.materia_prima_seleccionada["cantidad"] = cantidad
            self.materias_primas_seleccionadas.append(self.materia_prima_seleccionada.copy())
            
            self.actualizar_lista_mp_seleccionadas()
            
            self.busqueda.value = ""
            self.entry_cantidad.value = ""
            self.materia_prima_seleccionada = None
            self.page.update()
            
        except ValueError:
            self.mostrar_snack_bar("La cantidad debe ser un número")
    
    def actualizar_lista_mp_seleccionadas(self):
        if not hasattr(self, 'lista_mp_seleccionadas'):
            return
            
        self.lista_mp_seleccionadas.controls.clear()
        
        for mp in self.materias_primas_seleccionadas:
            self.lista_mp_seleccionadas.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{mp['nombre']}: {mp['cantidad']}", style=self.estilo_texto()),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="#a72d2d",
                            tooltip="Eliminar",
                            on_click=lambda e, mp=mp: self.eliminar_mp_de_lista(mp)
                        )
                    ]),
                    bgcolor="#fcc8a9",
                    border_radius=5,
                    padding=10,
                    margin=2
                )
            )
        self.page.update()
    
    def eliminar_mp_de_lista(self, mp):
        self.materias_primas_seleccionadas = [m for m in self.materias_primas_seleccionadas if m['id'] != mp['id']]
        self.actualizar_lista_mp_seleccionadas()
    
    def guardar_producto(self, e):
        nombre_producto = self.entrada_nombre_producto.value.strip() if hasattr(self, 'entrada_nombre_producto') else ""
        precio_texto = self.entrada_precio.value.strip() if hasattr(self, 'entrada_precio') else ""
        
        if not nombre_producto:
            self.mostrar_snack_bar("Ingresa un nombre para el producto")
            return
            
        if not precio_texto:
            self.mostrar_snack_bar("Ingresa un precio para el producto")
            return
            
        if not self.materias_primas_seleccionadas:
            self.mostrar_snack_bar("Agrega al menos una materia prima al producto")
            return
            
        try:
            precio = float(precio_texto)

            controlador = control_cargar_producto()
            try:
                id_producto = controlador.obtener_ultimo_id_producto()
                
                resultado = controlador.cargar_producto(id_producto, nombre_producto, precio)
                
                if resultado:
                    for mp in self.materias_primas_seleccionadas:
                        controlador.agregar_materia_prima_a_producto(
                            id_producto, 
                            mp["id"],
                            mp["cantidad"]
                        )
                    
                    self.mostrar_snack_bar(f"Producto '{nombre_producto}' guardado con éxito")
                    self.limpiar_formulario()
                else:
                    self.mostrar_snack_bar("Error al guardar el producto")
            finally:
                controlador.cerrar_conexion()
                
        except ValueError:
            self.mostrar_snack_bar("El precio debe ser un número")
    
    def limpiar_formulario(self):
        if hasattr(self, 'entrada_nombre_producto'):
            self.entrada_nombre_producto.value = ""
        if hasattr(self, 'entrada_precio'):
            self.entrada_precio.value = ""
        if hasattr(self, 'busqueda'):
            self.busqueda.value = ""
        if hasattr(self, 'entry_cantidad'):
            self.entry_cantidad.value = ""
            
        self.materias_primas_seleccionadas = []
        self.materia_prima_seleccionada = None
        self.actualizar_lista_mp_seleccionadas()
        self.page.update()
    
    def armar_vista(self):
        self.page.controls.clear()
        
        texto_carga_de_producto = ft.Text(
            "Cargar Producto y Receta",
            style=self.estilo_texto(),
            size=20
        )
        
        self.entrada_nombre_producto = ft.TextField(
            label="Nombre del Producto",
            hint_text="Ej: Pan de campo",
            hint_style=self.estilo_texto(),
            width=300,
            color="#37373A",
            border_color="#37373A",
            focused_border_color="#545454",
            label_style=ft.TextStyle(color="#37373A"),
        )
        
        self.entrada_precio = ft.TextField(
            label="Precio Unitario",
            hint_text="Ej: 500.50",
            hint_style=self.estilo_texto(),
            width=300,
            color="#37373A",
            border_color="#37373A",
            focused_border_color="#545454",
            label_style=ft.TextStyle(color="#37373A"),
        )
        
        self.busqueda = ft.TextField(
            label="Buscar Materia Prima",
            hint_text="Ingrese materia prima",
            width=300,
            color="#37373A",
            border_color="#37373A",
            focused_border_color="#545454",
            label_style=ft.TextStyle(color="#37373A"),
            on_change=self.filtrar_opciones
        )
        
        # Cantidad de materia prima
        self.entry_cantidad = ft.TextField(
            label="Cantidad",
            hint_text="Cantidad para la receta",
            width=300,
            color="#37373A",
            border_color="#37373A",
            focused_border_color="#545454",
            label_style=ft.TextStyle(color="#37373A"),
        )
        
        # Botón para agregar materia prima a la receta
        boton_agregar_mp = ft.ElevatedButton(
            "Agregar a Receta",
            width=150,
            style=self.estilo_de_botones(),
            on_click=self.agregar_materia_prima
        )
        
        # Lista de materias primas seleccionadas
        titulo_mp = ft.Text("Materias Primas de la Receta:", style=self.estilo_texto())
        self.lista_mp_seleccionadas = ft.Column(
            spacing=5,
            height=150,
            scroll="auto"
        )
        
        # Botón para guardar producto completo
        boton_guardar = ft.ElevatedButton(
            "Guardar Producto",
            width=200,
            style=self.estilo_de_botones(),
            on_click=self.guardar_producto
        )
        
        # Contenedor para datos del producto
        container_producto = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Datos del Producto", style=self.estilo_texto(), weight="bold"),
                    self.entrada_nombre_producto,
                    self.entrada_precio,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            padding=ft.padding.all(20),
            bgcolor="#fdd0b5",
            border_radius=10,
            width=350,
        )
        
        # Contenedor para la receta
        container_receta = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Agregar Materias Primas", style=self.estilo_texto(), weight="bold"),
                    self.busqueda,
                    self.resultados,
                    self.entry_cantidad,
                    boton_agregar_mp,
                    titulo_mp,
                    self.lista_mp_seleccionadas,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            padding=ft.padding.all(20),
            bgcolor="#fdd0b5",
            border_radius=10,
            width=350,
        )
        
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[self.boton_volver()],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            controls=[texto_carga_de_producto],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            controls=[container_producto, container_receta],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            controls=[boton_guardar],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                expand=True
            )
        )