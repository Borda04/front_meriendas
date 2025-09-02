import flet as ft

def mostrar_pantalla_principal(page):
    # Columna de opciones de Caídas
    columna_caidas = ft.Column([
        ft.Text("🧯 Caídas", size=24, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton("Ver Fechas de Caída", on_click=lambda e: page.go("/fechas")),
        ft.ElevatedButton("Agregar Voto", on_click=lambda e: page.go("/voto")),
    ], spacing=20)

    # Columna de opciones de Ajedrez
    columna_ajedrez = ft.Column([
        ft.Text("♟️ Ajedrez", size=24, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton("Fixture Ajedrez", on_click=lambda e: page.go("/fixture")),
        ft.ElevatedButton("Posiciones", on_click=lambda e: page.go("/puntajes")),
        ft.ElevatedButton("Ligas", on_click=lambda e: page.go("/ligas")),
        ft.ElevatedButton("Jugadores", on_click=lambda e: page.go("/jugadores")),
    ], spacing=20)

    def logout(e):
        page.client_storage.remove("auth_token")
        page.go("/")

    # Vista principal con dos columnas en una fila
    contenido_principal = ft.Column([
        ft.Text("🏠 Pantalla Principal", size=36, weight=ft.FontWeight.BOLD),
        ft.Row([
            columna_caidas,
            columna_ajedrez
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ft.ElevatedButton("Cerrar Sesión", on_click=logout, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=30)

    return contenido_principal
