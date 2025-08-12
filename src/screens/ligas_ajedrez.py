import flet as ft
from datetime import datetime
import requests

def mostrar_ligas_activas(page):
    ligas_container = ft.Column(scroll=ft.ScrollMode.AUTO)

    def cargar_ligas():
        try:
            response = requests.get("http://10.5.2.53:8103/consulta/ligas")
            data = response.json()

            if data.get("status") != "ok":
                ligas_container.controls.append(ft.Text("Error al obtener ligas", color=ft.Colors.RED))
                return

            ligas = data.get("data", [])

            ligas_container.controls.append(
                ft.Text("🏆 Ligas Actuales", size=24, weight=ft.FontWeight.BOLD)
            )

            if not ligas:
                ligas_container.controls.append(
                    ft.Text("No hay ligas activas en este momento.", color=ft.Colors.GREY)
                )
            else:
                for liga in ligas:
                    fecha_inicio = datetime.strptime(liga["FECHA_INICIO"].split(".")[0], "%Y-%m-%d %H:%M:%S")
                    fecha_inicio_str = fecha_inicio.strftime("%d/%m/%Y %H:%M")

                    fecha_fin_str = "En curso" if liga["FECHA_FIN"] is None else datetime.strptime(
                        liga["FECHA_FIN"].split(".")[0], "%Y-%m-%d %H:%M:%S"
                    ).strftime("%d/%m/%Y %H:%M")

                    ligas_container.controls.append(
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=ft.Column([
                                    ft.Text(f"{liga['NOMBRE']}", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Inicio: {fecha_inicio_str}"),
                                    ft.Text(f"Fin: {fecha_fin_str}", color=ft.Colors.GREEN if liga["FECHA_FIN"] is None else ft.Colors.GREY)
                                ])
                            )
                        )
                    )

            ligas_container.controls.append(
                ft.ElevatedButton("Volver al Inicio", on_click=lambda e: page.go("/"))
            )
            page.update()

        except Exception as e:
            ligas_container.controls.append(ft.Text(f"Error de conexión: {e}", color=ft.Colors.RED))
            page.update()

    page.views.append(
        ft.View(
            "/ligas",
            controls=[ligas_container],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_900,
        )
    )

    cargar_ligas()
