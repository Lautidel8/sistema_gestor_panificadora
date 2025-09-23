
import flet as ft
from frontend.controladores_front.configuracion_pantalla import configuracion_pantalla

class vista_controlar_stock(configuracion_pantalla):
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.config_page()
        self.armar_vista()
        
    def _load_materias_primas_datos(self):
        try:
            self.cursor.execute("""
                SELECT m.id_materia_prima, m.nombre_materia_prima, m.distribuidor, 
                    COALESCE(mp.cantidad, 0) as stock, u.nombre as unidad
                FROM MateriaPrima m
                LEFT JOIN MateriaPrima_Producto mp ON m.id_materia_prima = mp.id_materia_prima AND mp.id_producto = 1
                LEFT JOIN unidad u ON m.id_unidad = u.id_unidad
                ORDER BY m.nombre_materia_prima
            """)
            materias_primas = self.cursor.fetchall()
            self.materias_primas_data = materias_primas
        except Exception as e:
            print(f"Error cargando materias primas: {e}")
            self.materias_primas_data = []

    def _refresh_table_mp(self):
        """
        Actualiza la tabla de materias primas con los datos más recientes
        """
        if not self.mp_rows_container:
            return
        
        # Recargar datos por si hubo cambios
        self._load_materias_primas_datos()
        
        rows = []
        for mp in self.materias_primas_data:
            id_mp = mp[0]
            nombre = mp[1]
            distribuidor = mp[2]
            stock = mp[3]
            unidad = mp[4]
            
            # Formatear stock con 2 decimales
            stock_display = f"{float(stock):,.2f}" if stock is not None else "0.00"
            
            # Si hay una materia prima seleccionada, resaltarla
            selected = (self.mp_seleccionada is not None and self.mp_seleccionada[0] == id_mp)
            bg = "#ffc7a4" if selected else None
            
            rows.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(ft.Text(nombre, style=self.estilo_texto()), expand=True, padding=10),
                            ft.Container(ft.Text(distribuidor, style=self.estilo_texto()), expand=True, padding=10),
                            ft.Container(ft.Text(f"{stock_display} {unidad}", style=self.estilo_texto()), expand=True, padding=10),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    ),
                    bgcolor=bg,
                    on_click=lambda e, mp=mp: self.seleccionar_mp(e, mp)
                )
            )
        
        self.mp_rows_container.controls = rows
        self.page.update()

    def crear_header_mp(self):
        """
        Crea el encabezado para la tabla de materias primas
        """
        header = ft.Row(
            controls=[
                ft.Container(
                    ft.Text("Nombre", weight="bold", style=self.estilo_texto()), 
                    expand=True, padding=10, bgcolor="#ffc08d"
                ),
                ft.Container(
                    ft.Text("Distribuidor", weight="bold", style=self.estilo_texto()), 
                    expand=True, padding=10, bgcolor="#ffc08d"
                ),
                ft.Container(
                    ft.Text("Stock Disponible", weight="bold", style=self.estilo_texto()), 
                    expand=True, padding=10, bgcolor="#ffc08d"
                ),
            ],
            spacing=0
        )
        return header

    def seleccionar_mp(self, e, mp):
        """
        Maneja la selección de una materia prima en la grilla
        """
        if getattr(e, "data", None) is False:
            self.mp_seleccionada = None
        else:
            if self.mp_seleccionada is not None and self.mp_seleccionada[0] == mp[0]:
                self.mp_seleccionada = None
            else:
                self.mp_seleccionada = mp
        
        self._refresh_table_mp()
        self.page.update()
    

    def armar_vista(self):
        # Inicializar variables de control
        self.mp_seleccionada = None
        
        # Cargar datos
        self._load_materias_primas_datos()
        
        # Crear encabezado
        header = self.crear_header_mp()
        
        # Contenedor para las filas de materias primas
        self.mp_rows_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)
        self._refresh_table_mp()
        
        # Contenedor principal de la grilla
        grilla_mp = ft.Container(
            expand=True,
            bgcolor="#fdd0b5",
            content=ft.Column(
                [
                    header,
                    self.mp_rows_container,
                ],
                expand=True,
            ),
            height=550,
            width=1100,
            border_radius=10,
            padding=0,
        )
        
        # Texto de título
        titulo = ft.Text(
            "Control de Stock - Materias Primas",
            size=30,
            style=self.estilo_texto()
        )
        
        # Botones de acción
        boton_agregar_stock = ft.ElevatedButton(
            "Agregar Stock",
            width=150,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.page.go("/vista_carga_mp")
        )
        
        boton_volver = ft.ElevatedButton(
            "Volver",
            width=100,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.page.go("/vista_principal")
        )
        
        # Fila de título y botones
        titulo_row = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                titulo,
                ft.Row(
                    spacing=10,
                    controls=[boton_agregar_stock, boton_volver]
                )
            ]
        )
        
        # Armado de página completa
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        titulo_row,
                        grilla_mp
                    ],
                    expand=True,
                ),
                padding=20,
                expand=True
            )
        )
        