import flet as ft
import requests

from src.screens.login import mostrar_login
from src.screens.fechas import mostrar_pantalla_fechas
from src.screens.landing import mostrar_pantalla_principal
from src.screens.votacion import mostrar_pantalla_votacion
from src.screens.mostrar_pantalla_fixture import mostrar_pantalla_fixture_mejorado
from src.screens.pantalla_de_posiciones import mostrar_tabla_jugadores
from src.screens.participantes_ajedrez import mostrar_integrantes
from src.screens.ligas_ajedrez import mostrar_ligas_activas
from src.screens.dvd_screen import crear_fondo_dvd

def main(page: ft.Page):
    page.title = "Caidas"
    page.scroll = ft.ScrollMode.AUTO
    
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0

    # Contenedor para el contenido de la página actual
    page_content = ft.Container(expand=True)

    # Crear el fondo de DVD
    dvd_background = crear_fondo_dvd(page)

    # Estructura principal con Stack
    page.add(
        ft.Stack(
            [
                dvd_background,
                ft.Container(
                    content=page_content,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )
    )

    def route_change(e: ft.RouteChangeEvent):
        route = e.route
        token = page.client_storage.get("auth_token")

        public_routes = ["/"]

        if route not in public_routes and not token:
            page.go("/")
            return

        page_content.content = None  # Limpiar contenido anterior
        page_content.update()

        if route == "/":
            page_content.content = mostrar_login(page)
        elif route == "/app":
            page_content.content = mostrar_pantalla_principal(page)
        elif route == "/fechas":
            page_content.content = mostrar_pantalla_fechas(page)
        elif route == "/voto":
            page_content.content = mostrar_pantalla_votacion(page)
        elif route == "/jugadores":
            page_content.content = mostrar_integrantes(page)
        elif route == "/fixture":
            page_content.content = mostrar_pantalla_fixture_mejorado(page)
        elif route == "/puntajes":
            page_content.content = mostrar_tabla_jugadores(page)
        elif route == "/ligas":
            page_content.content = mostrar_ligas_activas(page)
        
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=8550, assets_dir="aset")

