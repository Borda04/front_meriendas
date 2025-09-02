import flet as ft
import requests
from datetime import datetime

def mostrar_integrantes(page):
    integrantes_container = ft.Column(scroll=ft.ScrollMode.AUTO)
    dropdown_integrante = ft.Dropdown(label="Filtrar por Nombre", on_change=lambda e: aplicar_filtro())

    integrantes = []

    def cargar_integrantes():
        nonlocal integrantes
        try:
            response = requests.get("http://10.5.2.53:8551/consulta/jugadores")
            #response = requests.get("localhost:8000/consulta/jugadores")
            data = response.json()

            if data.get("status") != "ok":
                integrantes_container.controls.append(ft.Text("Error al obtener integrantes", color=ft.Colors.RED))
                return

            integrantes = data.get("data", [])

            # Opciones del filtro
            nombres = sorted(set(j["NOMBRE"] for j in integrantes))
            dropdown_integrante.options = [ft.dropdown.Option(n) for n in nombres]

            aplicar_filtro()

        except Exception as e:
            integrantes_container.controls.append(ft.Text(f"Error de conexión: {e}", color=ft.Colors.RED))
            page.update()

    def aplicar_filtro():
        nombre_sel = dropdown_integrante.value

        integrantes_container.controls.clear()
        integrantes_container.controls.append(
            ft.Text("👥 Lista de Integrantes", size=22, weight=ft.FontWeight.BOLD)
        )

        filtro = [i for i in integrantes if not nombre_sel or i["NOMBRE"] == nombre_sel]

        if not filtro:
            integrantes_container.controls.append(
                ft.Text("No se encontraron integrantes para el filtro seleccionado.", color=ft.Colors.GREY)
            )
        else:
            for i in filtro:
                fecha = datetime.strptime(i["FECHA_REGISTRO"].split(".")[0], "%Y-%m-%d %H:%M:%S")
                email = i["EMAIL"] if i["EMAIL"] else "📭 No registrado"
                integrantes_container.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column([
                                ft.Text(f"{i['NOMBRE']} (ID: {i['ID_JUGADOR']})", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Email: {email}", color=ft.Colors.CYAN),
                                ft.Text(f"Fecha de Registro: {fecha.strftime('%d/%m/%Y %H:%M:%S')}")
                            ])
                        )
                    )
                )

        integrantes_container.controls.append(
            ft.ElevatedButton("Volver al Inicio", on_click=lambda e: page.go("/app"))
        )
        page.update()

    cargar_integrantes()

    return ft.Column(
        [
            ft.Row([dropdown_integrante], alignment=ft.MainAxisAlignment.START),
            integrantes_container
        ]
    )
