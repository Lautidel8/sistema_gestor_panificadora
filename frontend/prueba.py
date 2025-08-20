import flet as ft
import random
import time
import threading

def MyApp(page):
    x = 0

    slider1 = ft.Slider(value=30, min=0, max=100,
                        inactive_color="black", expand=True,
                        active_color="white")
    slider2 = ft.Slider(value=50, min=0, max=100,
                        inactive_color="black", expand=True,
                        active_color="white")
    slider3 = ft.Slider(value=20, min=0, max=100,
                        inactive_color="black", expand=True,
                        active_color="white")
    slider4 = ft.Slider(value=80, min=0, max=100,
                        inactive_color="black", expand=True,
                        active_color="white")

    indicator1 = ft.Text(value="30%", color="black")
    indicator2 = ft.Text(value="50%", color="black")
    indicator3 = ft.Text(value="20%", color="black")
    indicator4 = ft.Text(value="80%", color="black")

    control1 = ft.Row([slider1, indicator1], spacing=0, expand=True)
    control2 = ft.Row([slider2, indicator2], spacing=0, expand=True)
    control3 = ft.Row([slider3, indicator3], spacing=0, expand=True)
    control4 = ft.Row([slider4, indicator4], spacing=0, expand=True)

    data1 = [ft.LineChartData(data_points=[],
                              curved=True,
                              stroke_width=2,
                              color="black",
                              point=True,
                              )]

    graph1 = ft.LineChart(data_series=data1,
                          min_x=0,
                          max_x=50,
                          max_y=50,
                          min_y=0,
                          point_line_start=0,
                          expand=True,
                          interactive=False,
                          left_axis=ft.ChartAxis(visible=True, labels_size=30,),
                          bottom_axis=ft.ChartAxis(visible=True, labels_size=30,),
                          border=ft.Border(
                              bottom=ft.BorderSide(2, ft.Colors.with_opacity(0.3, "white")),
                              left=ft.BorderSide(2, ft.Colors.with_opacity(0.3, "white")),
                          ),
                          )

    data2 = [ft.LineChartData(data_points=[
                                ft.LineChartDataPoint(0, int(slider1.value)),
                                ft.LineChartDataPoint(25, int(slider2.value)),
                                ft.LineChartDataPoint(50, int(slider3.value)),
                                ft.LineChartDataPoint(100, int(slider4.value)),
                                ],
                                curved=True,
                                stroke_width=2,
                                color="black",
                                point=True,
                                below_line_gradient=ft.LinearGradient(["white", "purple"])
                              )]

    graph2 = ft.LineChart(data_series=data2,
                          min_x=0,
                          max_x=100,
                          min_y=0,
                          max_y=100,
                          point_line_start=0,
                          expand=True,
                          interactive=False,
                          border=ft.Border(
                              bottom=ft.BorderSide(2, ft.Colors.with_opacity(0.3, "white")),
                              left=ft.BorderSide(2, ft.Colors.with_opacity(0.3, "white")),
                          ),
                          )

    def value_slider1(e):
        indicator1.value = f"{int(slider1.value)} %"
        data2[0].data_points[0].y = slider1.value
        page.update()

    def value_slider2(e):
        indicator2.value = f"{int(slider2.value)} %"
        data2[0].data_points[1].y = slider2.value
        page.update()

    def value_slider3(e):
        indicator3.value = f"{int(slider3.value)} %"
        data2[0].data_points[2].y = slider3.value
        page.update()

    def value_slider4(e):
        indicator4.value = f"{int(slider4.value)} %"
        data2[0].data_points[3].y = slider4.value
        page.update()

    slider1.on_change = value_slider1
    slider2.on_change = value_slider2
    slider3.on_change = value_slider3
    slider4.on_change = value_slider4

    def real_time_data():
        nonlocal x
        while True:
            x += 1
            data = random.randint(5, 45)
            data1[0].data_points.append(ft.LineChartDataPoint(x, data))

            if len(data1[0].data_points) == 50:
                x = 0
                data1[0].data_points.clear()
            page.update()
            time.sleep(0.3)

    threading.Thread(target=real_time_data, daemon=True).start()

    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(["purple", "white"], rotation=30),
                border_radius=10,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            height=60,
                            padding=10,
                            alignment=ft.alignment.center,
                            content=ft.Text("Gráfica en tiempo real",
                                            color="black",
                                            font_family="vivaldi",
                                            size=30,
                                            weight="bold")
                        ),
                        ft.Container(
                            expand=True,
                            content=graph1,
                            padding=20,
                        )
                    ]
                )
            ),
            ft.Container(
                gradient=ft.LinearGradient(["purple", "white"]),
                expand=True,
                border_radius=10,
                padding=10,
                content=ft.Row(
                    spacing=20,
                    controls=[
                        ft.Column(
                            expand=True,
                            controls=[
                                control1,
                                control2,
                                control3,
                                control4,
                            ]
                        ),
                        ft.Column(
                            expand=True,
                            controls=[
                                graph2
                            ]
                        )
                    ]
                )
            ),
        ]
    )

def main(page: ft.Page):
    page.add(MyApp(page))

ft.app(target=main)