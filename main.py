import flet as ft
import requests

from src.screens.fechas import mostrar_pantalla_fechas
from src.screens.landing import mostrar_pantalla_principal
from src.screens.votacion import mostrar_pantalla_votacion
from src.screens.mostrar_pantalla_fixture import mostrar_pantalla_fixture_mejorado
from src.screens.pantalla_de_posiciones import mostrar_tabla_jugadores
from src.screens.participantes_ajedrez import mostrar_integrantes
from src.screens.ligas_ajedrez import mostrar_ligas_activas

def main(page: ft.Page):
    page.title = "Caidas"
    page.scroll = ft.ScrollMode.AUTO
    page.update()
   
    #mostrar_pantalla_principal(page)

    #mostrar_pantalla_fechas(page)

    #mostrar_pantalla_votacion(page)

    # Manejador de rutas
    def route_change(e: ft.RouteChangeEvent):
        route = e.route
        if route == "/":
            mostrar_pantalla_principal(page)
        elif route == "/fechas":
            mostrar_pantalla_fechas(page)
        elif route == "/voto":
            mostrar_pantalla_votacion(page)
        elif route == "/jugadores":
            mostrar_integrantes(page)
        elif route == "/fixture":
            mostrar_pantalla_fixture_mejorado(page)
        elif route == "/puntajes":
            mostrar_tabla_jugadores(page)
        elif route == "/ligas":
            mostrar_ligas_activas(page)
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

# Ejecutar la app
# ft.app(target=main)

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)

