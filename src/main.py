import flet as ft

from components.tarjeta import Tarjeta
from components.inputs import Visor

def main(page: ft.Page):
    page.title = "Administrador de Tareas"
    page.padding = 16
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_50
    page.window.width = 1180
    page.window.height = 660

    tarjeta = Tarjeta(page)
    visor = Visor(page, tarjeta)

    def _create():
        return ft.Column(
            controls=[visor.build_inputs(), tarjeta.build_tarjeta()],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
            spacing=12,
        )

    page.add(_create())

ft.run(main)