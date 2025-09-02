import flet as ft
import requests
from collections import defaultdict

def mostrar_pantalla_fixture_mejorado(page):
    fixture_container = ft.Column(scroll=ft.ScrollMode.AUTO)
    dropdown_ronda = ft.Dropdown(label="Filtrar por Ronda", on_change=lambda e: aplicar_filtros())
    dropdown_jugador = ft.Dropdown(label="Filtrar por Jugador", on_change=lambda e: aplicar_filtros())
    partidas_totales = []

    def cargar_fixture():
        nonlocal partidas_totales

        try:
            response = requests.get("http://10.5.2.53:8551/consulta/fixture_rondas")
            #response = requests.get("http://localhost:8000/consulta/fixture_rondas")
            json_data = response.json()

            if json_data.get("status") != "ok":
                fixture_container.controls.clear()
                fixture_container.controls.append(ft.Text("Error al obtener fixture", color=ft.Colors.RED))
                return

            partidas_totales = json_data.get("data", [])

            dropdown_ronda.options = sorted(
                list({ft.dropdown.Option(p["RONDA"]) for p in partidas_totales}),
                key=lambda o: int(o.key or o.value)
            )

            jugadores = sorted(list({p["JUGADOR_BLANCO"] for p in partidas_totales} | {p["JUGADOR_NEGRO"] for p in partidas_totales}))
            dropdown_jugador.options = [ft.dropdown.Option(j) for j in jugadores]

            aplicar_filtros()

        except Exception as e:
            fixture_container.controls.clear()
            fixture_container.controls.append(ft.Text(f"Error de conexión: {e}", color=ft.Colors.RED))

    def aplicar_filtros():
        ronda_sel = dropdown_ronda.value
        jugador_sel = dropdown_jugador.value

        fixture_container.controls.clear()
        fixture_container.controls.append(
            ft.Text("🎯 Fixture del Torneo", size=22, weight=ft.FontWeight.BOLD)
        )

        # Filtrado de partidas
        filtro = [
            p for p in partidas_totales
            if (not ronda_sel or p["RONDA"] == ronda_sel)
            and (not jugador_sel or jugador_sel in [p["JUGADOR_BLANCO"], p["JUGADOR_NEGRO"]])
        ]

        if not filtro:
            fixture_container.controls.append(ft.Text("No hay partidas para el filtro seleccionado.", color=ft.Colors.GREY))
        else:
            # Agrupar por ronda
            por_ronda = defaultdict(list)
            for p in filtro:
                por_ronda[p["RONDA"]].append(p)

            # Ordenar rondas
            for ronda in sorted(por_ronda.keys(), key=lambda x: int(x)):
                fixture_container.controls.append(
                    ft.Text(f"🏁 Ronda {ronda}", size=18, weight=ft.FontWeight.BOLD)
                )

                row_partidas = ft.ResponsiveRow(run_spacing=10, spacing=10)

                

                for p in por_ronda[ronda]:
                    estado = "Jugado" if p["RESULTADO"] else "Pendiente"
                    color_estado = ft.Colors.GREEN if estado == "Jugado" else ft.Colors.AMBER_700

                    card = ft.Container(
                        bgcolor=ft.Colors.BLUE_GREY_800,
                        padding=12,
                        border_radius=12,
                        content=ft.Column([
                            ft.Text(f"{p['JUGADOR_BLANCO']} ⚪ vs ⚫ {p['JUGADOR_NEGRO']}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Text(f"Resultado: {p['RESULTADO'] or '🕓 Pendiente'}", size=14),
                            ft.Text(f"Estado: {estado}", color=color_estado, size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Fecha: {p['FECHA_PARTIDA']}", size=12, italic=True),
                        ])
                    )

                    row_partidas.controls.append(
                        ft.Container(content=card, col=3)  # 3 => 4 columnas por fila
                    )

                fixture_container.controls.append(row_partidas)
                fixture_container.controls.append(ft.Divider(height=30))

        fixture_container.controls.append(
            ft.ElevatedButton(
                "Volver al Inicio",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: page.go("/app")
            )
        )
        page.update()

    cargar_fixture()

    return ft.Column(
        [
            ft.Container(
                padding=10,
                content=ft.ResponsiveRow([
                    ft.Container(dropdown_ronda, col=6),
                    ft.Container(dropdown_jugador, col=6),
                ])
            ),
            fixture_container
        ]
    )
