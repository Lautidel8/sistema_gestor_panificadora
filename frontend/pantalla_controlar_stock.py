
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
                    m.stock, u.nombre as unidad
                FROM MateriaPrima m
                LEFT JOIN unidad u ON m.id_unidad = u.id_unidad
                ORDER BY m.nombre_materia_prima
            """)
            materias_primas = self.cursor.fetchall()
            self.materias_primas_data = materias_primas
        except Exception as e:
            print(f"Error cargando materias primas: {e}")
            self.materias_primas_data = []

    def _refresh_table_mp(self):

        if not self.mp_rows_container:
            return
        
        
        self._load_materias_primas_datos()
        
        rows = []
        for mp in self.materias_primas_data:
            id_mp = mp[0]
            nombre = mp[1]
            distribuidor = mp[2]
            stock = mp[3]
            unidad = mp[4]
            
            stock_display = f"{float(stock):,.2f}" if stock is not None else "0.00"
            

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
                )
            )
        
        self.mp_rows_container.controls = rows
        self.page.update()

    def crear_header_mp(self):
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


    def armar_vista(self):

        self.mp_seleccionada = None

        self._load_materias_primas_datos()
        
        header = self.crear_header_mp()
        
        self.mp_rows_container = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)
        self._refresh_table_mp()
        
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
            height=490,
            width=1100,
            border_radius=10,
            padding=0,
        )

        titulo = ft.Text(
            "Control de Stock de Materia Prima",
            size=30,
            style=self.estilo_texto()
        )
        
        boton_agregar_stock = ft.ElevatedButton(
            "Agregar Stock",
            width=150,
            style=self.estilo_de_botones(),
            on_click=lambda e: self.page.go("/vista_carga_mp")
        )
        
        fila_boton_volver = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
            controls=[self.boton_volver()]
        )

        titulo_row = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                titulo,
                ft.Row(
                    spacing=10,
                    controls=[boton_agregar_stock]
                )
            ]
        )
        
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        fila_boton_volver,
                        titulo_row,
                        grilla_mp
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=20,
                expand=True
            )
        )
        