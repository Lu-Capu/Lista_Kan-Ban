import flet as ft

class Tarea:

    COLORES_PRIORIDAD = {
        "Alta": ft.Colors.RED_800,
        "Media": ft.Colors.ORANGE_800,
        "Baja": ft.Colors.GREEN_800,
    }

    COLORES_BORDE = {
        "Alta": ft.Colors.RED_300,
        "Media": ft.Colors.AMBER_300,
        "Baja": ft.Colors.GREEN_300,
    }

    def __init__(self, texto: str, page: ft.Page, prioridad: str, estado: str = "Pendiente"):
        self.page = page
        self.texto = texto
        self._estado = estado
        self.prioridad = prioridad

        self.txt_estado = ft.Text(
            "Estado: " + self._estado,
            size=15,
            selectable=True,
            color=ft.Colors.WHITE,
        )

        self.txt_fantasma_estado = ft.Text(
            "Estado: " + self._estado,
            size=14,
            color=ft.Colors.WHITE,
        )

        # Contenedor PROPIO y visible de cada tarea con color según su prioridad
        self.contenido = ft.Container(
            padding=12,
            border_radius=8,
            bgcolor=self._color_fondo(),
            border=ft.Border.all(1.5, self._color_borde()),
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(
                        "Tarea: " + self.texto,
                        size=15,
                        weight=ft.FontWeight.W_600,
                        selectable=True,
                        color=ft.Colors.WHITE,
                    ),
                    self.txt_estado,
                    ft.Text(
                        "Prioridad: " + self.prioridad,
                        size=15,
                        selectable=True,
                        color=ft.Colors.WHITE,
                    ),
                    # Aquí luego se agregan más atributos
                ],
            ),
        )

        # El Draggable es el control que viaja entre tarjetas.
        # data=self permite recuperar este objeto al soltarlo.
        self.control = ft.Draggable(
            content=self.contenido,
            group="tareas",
            data=self,
            max_simultaneous_drags=1,
            content_feedback=self._fantasma(),
            content_when_dragging=self._placeholder(),
        )

    def _color_fondo(self) -> str:
        return self.COLORES_PRIORIDAD.get(self.prioridad, ft.Colors.BLACK)

    def _color_borde(self) -> str:
        return self.COLORES_BORDE.get(self.prioridad, ft.Colors.BLACK_26)

    def _fantasma(self) -> ft.Container:
        return ft.Container(
            width=280,
            padding=12,
            border_radius=8,
            bgcolor=self._color_fondo(),
            border=ft.Border.all(1.5, self._color_borde()),
            opacity=0.75,
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(
                        "Tarea: " + self.texto,
                        size=15,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.WHITE,
                    ),
                    self.txt_fantasma_estado,
                    ft.Text(
                        "Prioridad: " + self.prioridad,
                        size=14,
                        color=ft.Colors.WHITE,
                    ),
                ],
            ),
        )

    def _placeholder(self) -> ft.Container:
        return ft.Container(
            padding=12,
            border_radius=8,
            border=ft.Border.all(1, self._color_borde()),
            opacity=0.35,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                "Moviendo...",
                size=13,
                italic=True,
                color=ft.Colors.WHITE,
            ),
        )

    def build(self) -> ft.Draggable:
        return self.control

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str):
        self._estado = valor
        if hasattr(self, "txt_estado"):
            self.txt_estado.value = "Estado: " + valor
        if hasattr(self, "txt_fantasma_estado"):
            self.txt_fantasma_estado.value = "Estado: " + valor
