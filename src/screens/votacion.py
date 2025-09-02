import flet as ft
import requests

def obtener_empleados():
    response = requests.get("http://10.5.2.53:8551/consulta/integrantes")
    #response = requests.get("http://localhost:8000/consulta/integrantes")
    json_data = response.json()
    datos = json_data.get("data", [])
    return [
        ft.dropdown.Option(key=emp['ID'], text=emp['NOMBRE']) for emp in datos
    ]

def obtener_id_caidas():
    response = requests.get("http://10.5.2.53:8551/consulta/fechas")
    #response = requests.get("http://localhost:8000/consulta/fechas")
    json_data = response.json()
    datos_caida = json_data.get("data", [])
    return [
        ft.dropdown.Option(key=caida['ID'], text=f"ID #{caida['ID']}") for caida in datos_caida
    ]

def guardar_votos(id_caida, id_integrante, valor_voto, page):
    payload = {
        "id_caida": str(id_caida),
        "id_empleado": str(id_integrante),
        "valor_voto": str(valor_voto)
    }

    try:
        response = requests.post("http://10.5.2.53:8551/votacion/votar", json=payload)
        #response = requests.post("http://localhost:8000/votacion/votar", json=payload)
        json_data = response.json()
        msg = json_data.get("message", "Voto registrado correctamente")
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN_400)
    except Exception as e:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"), bgcolor=ft.Colors.RED)
    
    page.snack_bar.open = True
    page.update()

def mostrar_pantalla_votacion(page):
    db_caida = ft.Dropdown(
        label='Seleccioná una caída',
        options=obtener_id_caidas(),
        width=300
    )

    db_empleado = ft.Dropdown(
        label='Seleccioná tu nombre',
        options=obtener_empleados(),
        width=300
    )

    s_valor_voto = ft.Slider(
        min=0, max=10, divisions=10,
        label="{value}",
        active_color=ft.Colors.CYAN,
        thumb_color=ft.Colors.CYAN_ACCENT
    )

    btn_guardar = ft.ElevatedButton(
        text="Guardar Voto 📝",
        icon=ft.Icons.SAVE,
        on_click=lambda e: guardar_votos(db_caida.value, db_empleado.value, s_valor_voto.value, page)
    )

    card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Registro de Votación", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                db_caida,
                db_empleado,
                ft.Text("Calificá la caída", size=16),
                s_valor_voto,
                btn_guardar,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )

    volver_btn = ft.ElevatedButton("← Volver", icon=ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/app"))

    return ft.Column(
        [
            ft.Container(content=card, alignment=ft.alignment.center),
            volver_btn
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
