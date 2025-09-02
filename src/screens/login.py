
import flet as ft
import requests

def mostrar_login(page: ft.Page):
    username = ft.TextField(
        hint_text="Email ID",
        prefix_icon=ft.Icons.PERSON,
        border_radius=10,
        bgcolor=ft.Colors.BLACK,
        width=300
    )

    password = ft.TextField(
        hint_text="Password",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        border_radius=10,
        bgcolor=ft.Colors.BLACK,
        width=300
    )

    error_text = ft.Text("", color=ft.Colors.RED)
    loading = ft.ProgressRing(visible=False)

    def login_click(e):
        error_text.value = ""
        loading.visible = True
        page.update()

        try:
            response = requests.post(
                "http://10.5.2.53:8551/auth/login",
                json={"username": username.value, "password": password.value}
            )
            if response.status_code == 200:
                print (response.json())
                token = response.json().get("access_token")
                if token:
                    page.client_storage.set("auth_token", token)
                    page.go("/app")
                else:
                    error_text.value = "Login successful, but no token received."
            else:
                error_text.value = "Invalid credentials"
        except Exception as ex:
            error_text.value = f"Connection error: {ex}"

        loading.visible = False
        page.update()

    login_card = ft.Container(
        alignment=ft.alignment.center,
        height=350,
        width=450,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border_radius=20,
        padding=30,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.WHITE),
                    padding=10
                ),
                username,
                password,
                ft.ElevatedButton(
                    "LOGIN",
                    width=300,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        bgcolor={"": "#0866f3"},
                        color=ft.Colors.WHITE
                    ),
                    on_click=login_click
                ),
                error_text,
                loading,
            ]
        )
    )

    return ft.Container(
        alignment=ft.alignment.center,
        content=login_card,
        expand=True
    )

