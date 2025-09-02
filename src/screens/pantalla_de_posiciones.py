import flet as ft
import requests

def mostrar_tabla_jugadores(page):
    jugadores_container = ft.Column(scroll=ft.ScrollMode.AUTO)

    def cargar_jugadores():
        try:
            response = requests.get("http://10.5.2.53:8551/consulta/puntajes")
            #response = requests.get("localhost:8000/consulta/puntajes")
            data = response.json()

            if data.get("status") != "ok":
                jugadores_container.controls.append(ft.Text("Error al obtener jugadores", color=ft.Colors.RED))
                return

            jugadores = data.get("data", [])
            jugadores_container.controls.append(
                ft.Text("📋 Tabla de Jugadores", size=22, weight=ft.FontWeight.BOLD)
            )

            if not jugadores:
                jugadores_container.controls.append(ft.Text("No hay jugadores cargados.", color=ft.Colors.GREY))
            else:
                for j in sorted(jugadores, key=lambda x: int(x["PUNTAJE"]), reverse=True):
                    jugadores_container.controls.append(
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=ft.Column([
                                    ft.Text(f"{j['NOMBRE']} (ID: {j['ID_JUGADOR']})", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Row([
                                        ft.Text(f"Jugado: {j['JUGADO']}"),
                                        ft.Text(f"Ganado: {j['GANADO']}"),
                                        ft.Text(f"Empatado: {j['EMPATADO']}"),
                                        ft.Text(f"Perdido: {j['PERDIDO']}"),
                                        ft.Text(f"Puntaje: {j['PUNTAJE']}", weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_200),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                ])
                            )
                        )
                    )

            jugadores_container.controls.append(
                ft.ElevatedButton("Volver al Inicio", on_click=lambda e: page.go("/app"))
            )

            page.update()

        except Exception as e:
            jugadores_container.controls.append(ft.Text(f"Error de conexión: {e}", color=ft.Colors.RED))
            page.update()

    cargar_jugadores()

    return jugadores_container
