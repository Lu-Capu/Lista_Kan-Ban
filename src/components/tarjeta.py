import flet as ft
from components.tarea import Tarea
GRUPO = "tareas"


class Tarjeta:

    TITULOS = ["Pendiente", "En proceso", "Completada"]
    ESTADOS = ["Pendiente", "En proceso", "Completada"]
    COLORES = [ft.Colors.RED_200, ft.Colors.AMBER_200, ft.Colors.GREEN_200]
    COLOR_RESALTE = ft.Colors.BLUE_100

    def __init__(self, page: ft.Page):
        self.page = page
        self.columnas = [
            ft.Column(
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            )
            for _ in range(len(self.TITULOS))
        ]
        # Tarjetas creadas una sola vez para poder resaltarlas/restaurarlas
        self.tarjetas = [
            self._create(i) for i in range(len(self.columnas))
        ]
        self._resaltado: int | None = None

    def _create(self, indice: int) -> ft.Card:
        contenido_tarjeta = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            self.TITULOS[indice],
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK_87,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(color=ft.Colors.BLACK_26, height=1),
                self.columnas[indice],
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        objetivo = ft.DragTarget(
            content=contenido_tarjeta,
            group=GRUPO,
            on_will_accept=lambda e: self._will_accept(e, indice),
            on_leave=lambda e: self._leave(e, indice),
            on_accept=lambda e: self._accept(e, indice),
        )
        return ft.Card(
            content=ft.Container(
                padding=16,
                content=objetivo,
                expand=True,
            ),
            bgcolor=self.COLORES[indice],
            expand=True,
        )

    # ---------- arrastrar y soltar ----------

    def _will_accept(self, e, indice: int):
        e.accept = True
        self._resaltar(indice)

    def _leave(self, e, indice: int):
        self._restaurar(indice)

    def _accept(self, e, indice: int):
        self._restaurar(indice)
        if hasattr(e, "src") and e.src and hasattr(e.src, "data"):
            tarea = e.src.data
            if isinstance(tarea, Tarea):
                self.mover(tarea, indice)

    def _resaltar(self, indice: int):
        if self._resaltado == indice:
            return
        self._restaurar()
        self.tarjetas[indice].bgcolor = self.COLOR_RESALTE
        self._resaltado = indice
        self.page.update()

    def _restaurar(self, indice: int | None = None):
        indice = self._resaltado if indice is None else indice
        if indice is None or self._resaltado != indice:
            return
        self.tarjetas[indice].bgcolor = self.COLORES[indice]
        self._resaltado = None
        self.page.update()

    # ---------- movimientos ----------

    def agregar(self, tarea: Tarea, destino: int = 0):
        self.columnas[destino].controls.insert(0, tarea.build())
        self.page.update()

    def mover(self, tarea: Tarea, destino: int):
        control = tarea.build()
        for columna in self.columnas:
            if control in columna.controls:
                columna.controls.remove(control)
                break
        tarea.estado = self.ESTADOS[destino]
        self.columnas[destino].controls.insert(0, control)
        self.page.update()

    def build_tarjeta(self):
        return ft.Row(
            controls=self.tarjetas,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
