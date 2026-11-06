import flet as ft

from components.tarea import Tarea

GRUPO = "tareas"


class Tarjeta:

    TITULOS = ["Pendiente", "En proceso", "Completada"]
    ESTADOS = ["Pendiente", "En proceso", "Completada"]

    # Colores muy suaves para las columnas y un acento por estado.
    FONDOS = [ft.Colors.RED_50, ft.Colors.AMBER_50, ft.Colors.GREEN_50]
    BORDES = [ft.Colors.RED_200, ft.Colors.AMBER_200, ft.Colors.GREEN_200]
    ACENTOS = [ft.Colors.RED_400, ft.Colors.AMBER_600, ft.Colors.GREEN_400]

    COLOR_RESALTE = ft.Colors.BLUE_50
    ACENTO_RESALTE = ft.Colors.BLUE_400

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
        # Contenedores de cada columna, para cambiarles el borde al resaltar.
        self.contenedores = []
        # Tarjetas creadas una sola vez para poder resaltarlas/restaurarlas
        self.tarjetas = [
            self._create(i) for i in range(len(self.columnas))
        ]
        self._resaltado: int | None = None

    def _create(self, indice: int) -> ft.Card:
        encabezado = ft.Row(
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=8,
                    height=8,
                    border_radius=4,
                    bgcolor=self.ACENTOS[indice],
                ),
                ft.Text(
                    self.TITULOS[indice],
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.BLACK_87,
                ),
            ],
        )

        contenido_tarjeta = ft.Column(
            controls=[
                encabezado,
                ft.Divider(color=ft.Colors.GREY_200, height=1),
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

        contenedor = ft.Container(
            padding=16,
            content=objetivo,
            expand=True,
            bgcolor=self.FONDOS[indice],
            border=ft.Border.all(1, self.BORDES[indice]),
            border_radius=12,
        )
        self.contenedores.append(contenedor)

        return ft.Card(
            content=contenedor,
            bgcolor=self.FONDOS[indice],
            elevation=0,
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
        contenedor = self.contenedores[indice]
        contenedor.bgcolor = self.COLOR_RESALTE
        contenedor.border = ft.Border.all(2, self.ACENTO_RESALTE)
        self._resaltado = indice
        self.page.update()

    def _restaurar(self, indice: int | None = None):
        indice = self._resaltado if indice is None else indice
        if indice is None or self._resaltado != indice:
            return
        contenedor = self.contenedores[indice]
        contenedor.bgcolor = self.FONDOS[indice]
        contenedor.border = ft.Border.all(1, self.BORDES[indice])
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
