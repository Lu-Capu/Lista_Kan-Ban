import flet as ft


class Tarea:

    # Cada prioridad tiene su icono y su color, pero el color se usa
    # solo en la etiqueta para no saturar la tarjeta.
    ICONOS_PRIORIDAD = {
        "Alta": ft.Icons.ARROW_UPWARD,
        "Media": ft.Icons.REMOVE,
        "Baja": ft.Icons.ARROW_DOWNWARD,
    }

    COLORES_PRIORIDAD = {
        "Alta": ft.Colors.RED_700,
        "Media": ft.Colors.ORANGE_800,
        "Baja": ft.Colors.GREEN_700,
    }

    FONDOS_PRIORIDAD = {
        "Alta": ft.Colors.RED_50,
        "Media": ft.Colors.ORANGE_50,
        "Baja": ft.Colors.GREEN_50,
    }

    def __init__(self, texto: str, page: ft.Page, prioridad: str, estado: str = "Pendiente"):
        self.page = page
        self.texto = texto
        self._estado = estado
        self.prioridad = prioridad

        self.txt_estado = ft.Text(
            self._estado,
            size=12,
            selectable=True,
            color=ft.Colors.BLACK_45,
        )

        self.txt_fantasma_estado = ft.Text(
            self._estado,
            size=12,
            color=ft.Colors.BLACK_45,
        )

        # La tarjeta de la tarea se mantiene blanca para que el color
        # quede solo en la etiqueta de prioridad.
        self.contenido = ft.Container(
            padding=12,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        self.texto,
                        size=15,
                        weight=ft.FontWeight.W_600,
                        selectable=True,
                        color=ft.Colors.BLACK_87,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self._etiqueta_prioridad(),
                            self.txt_estado,
                        ],
                    ),
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

    def _etiqueta_prioridad(self) -> ft.Container:
        color = self._color_prioridad()
        return ft.Container(
            padding=ft.Padding(8, 3, 10, 3),
            border_radius=20,
            bgcolor=self._fondo_prioridad(),
            content=ft.Row(
                tight=True,
                spacing=3,
                controls=[
                    ft.Icon(self._icono_prioridad(), size=15, color=color),
                    ft.Text(
                        self.prioridad,
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=color,
                    ),
                ],
            ),
        )

    def _icono_prioridad(self) -> str:
        return self.ICONOS_PRIORIDAD.get(self.prioridad, ft.Icons.REMOVE)

    def _color_prioridad(self) -> str:
        return self.COLORES_PRIORIDAD.get(self.prioridad, ft.Colors.BLACK_54)

    def _fondo_prioridad(self) -> str:
        return self.FONDOS_PRIORIDAD.get(self.prioridad, ft.Colors.GREY_100)

    def _fantasma(self) -> ft.Container:
        return ft.Container(
            width=280,
            padding=12,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_400),
            opacity=0.95,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.BLACK_26,
                offset=ft.Offset(0, 3),
            ),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        self.texto,
                        size=15,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.BLACK_87,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self._etiqueta_prioridad(),
                            self.txt_fantasma_estado,
                        ],
                    ),
                ],
            ),
        )

    def _placeholder(self) -> ft.Container:
        return ft.Container(
            padding=12,
            border_radius=10,
            bgcolor=ft.Colors.GREY_100,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            opacity=0.6,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                "Moviendo...",
                size=13,
                italic=True,
                color=ft.Colors.BLACK_45,
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
            self.txt_estado.value = valor
        if hasattr(self, "txt_fantasma_estado"):
            self.txt_fantasma_estado.value = valor
