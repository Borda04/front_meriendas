import flet as ft
import requests

def mostrar_pantalla_fechas(page):
    tabla_container = ft.Column(
        [ft.Text("⏳ Cargando datos...", size=18, italic=True)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25
    )

    def cargar_datos():
        try:
            response = requests.get("http://10.5.2.53:8103/consulta/fechas")
            json_data = response.json()

            if json_data.get("status") != "ok":
                tabla_container.controls.clear()
                tabla_container.controls.append(
                    ft.Text("❌ Error: respuesta no válida", color=ft.Colors.RED, size=16)
                )
                return

            datos = json_data.get("data", [])

            if not datos:
                tabla_container.controls.clear()
                tabla_container.controls.append(
                    ft.Text("⚠️ No hay fechas disponibles.", color=ft.Colors.GREY)
                )
                return

            tabla = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nombre 1")),
                    ft.DataColumn(ft.Text("Nombre 2")),
                    ft.DataColumn(ft.Text("Fecha")),
                    ft.DataColumn(ft.Text("Menú")),
                    ft.DataColumn(ft.Text("Puntuación")),
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Faltan...")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(d.get("ID", "")))),
                            ft.DataCell(ft.Text(d.get("NOMBRE_EMPLEADO_1", ""))),
                            ft.DataCell(ft.Text(d.get("NOMBRE_EMPLEADO_2", ""))),
                            ft.DataCell(ft.Text(d.get("FECHA_CAIDA", ""))),
                            ft.DataCell(ft.Text(str(d.get("MENU", "-")) if d.get("MENU") else "-")),
                            ft.DataCell(ft.Text(str(d.get("PUNTUACION", "-")) if d.get("PUNTUACION") else "-")),
                            ft.DataCell(
                                ft.Row([
                                    ft.Icon(
                                        name=ft.Icons.CHECK_CIRCLE if str(d.get("ESTADO")).lower() == "y" else ft.Icons.CANCEL,
                                        color=ft.Colors.GREEN if str(d.get("ESTADO")).lower() == "y" else ft.Colors.RED,
                                    ),
                                    ft.Text("DEGUSTADO" if str(d.get("ESTADO")).lower() == "y" else "INACTIVO")
                                ])
                            ),
                            ft.DataCell(
                                ft.Text(f"Faltan {d.get('FALTAN_X_DIAS', '-')} días")
                            ),
                        ]
                    )
                    for d in datos
                ],
                heading_row_color=ft.Colors.BLUE_GREY_800,
                data_row_color={"even": ft.Colors.BLUE_GREY_700, "odd": ft.Colors.BLUE_GREY_800},
                divider_thickness=0.5,
                show_bottom_border=True
            )

            tabla_container.controls.clear()
            tabla_container.controls.append(
                ft.Text("📅 Tabla de Fechas", size=26, weight=ft.FontWeight.BOLD)
            )
            tabla_container.controls.append(
                ft.Row([tabla], alignment=ft.MainAxisAlignment.CENTER)
            )
            tabla_container.controls.append(
                ft.ElevatedButton("🔙 Volver al Inicio", on_click=lambda e: page.go("/"))
            )
            page.update()

        except Exception as e:
            tabla_container.controls.clear()
            tabla_container.controls.append(
                ft.Text(f"🚫 Error al conectar: {e}", color=ft.Colors.RED)
            )
            page.update()

    cargar_datos()

    page.views.append(
        ft.View(
            "/fechas",
            controls=[tabla_container],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_900,
            padding=20,
        )
    )
