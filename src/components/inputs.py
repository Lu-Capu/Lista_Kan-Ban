import flet as ft

from components.tarjeta import Tarjeta
from components.tarea import Tarea

class Visor():

    def __init__(self, page: ft.Page, tarjeta: Tarjeta):
        self.page = page
        self.tarjeta = tarjeta

    def _create_widgets(self):
        lbl = ft.Text("Ingrese una tarea: ", weight=ft.FontWeight.W_500, size=15)
        
        self.txt = ft.TextField(
            label="Tarea",
            hint_text="Ingresar la tarea",
            on_submit=self.on_click,
            expand=True,
        )
        
        # Guardamos combo en self para acceder a él en on_click
        self.combo = ft.Dropdown(
            label="Prioridad",
            hint_text="Selecciona...",
            width=150,
            options=[
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Media"),
                ft.dropdown.Option("Baja"),
            ],
            on_select=self.al_cambiar
        )
        
        btn = ft.Button(
            "Agregar",
            icon=ft.Icons.ADD_TASK,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self.on_click,
        )
        
        self.lbl_mensaje = ft.Text("", size=13)
        
        return ft.Container(
            content=ft.Row(
                # Agregamos self.combo a las controles del Row
                controls=[lbl, self.txt, self.combo, btn, self.lbl_mensaje],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(0, 0, 0, 8),
        )

    # Método de clase recibiendo self
    def al_cambiar(self, e):
        if self.combo.value:
            self.lbl_mensaje.value = f"Prioridad elegida: {self.combo.value}"
            self.lbl_mensaje.color = ft.Colors.BLUE_700
            self.lbl_mensaje.update()
        
    def on_click(self, e):
        tarea = self.txt.value
        prioridad = self.combo.value

        if not tarea or not tarea.strip():
            self.lbl_mensaje.value = "Ingrese una tarea"
            self.lbl_mensaje.color = ft.Colors.RED_700
            self.lbl_mensaje.update()
            return
        if not prioridad:
            self.lbl_mensaje.value = "Ingrese una prioridad"
            self.lbl_mensaje.color = ft.Colors.RED_700
            self.lbl_mensaje.update()
            return
        
        #envio de la tarea
        self.tarjeta.agregar(Tarea(tarea.strip(), self.page, prioridad))
        
        self.txt.value = ""
        self.combo.value = None
        
        self.lbl_mensaje.value = "Tarea agregada"
        self.lbl_mensaje.color = ft.Colors.GREEN_700
        self.update()

    def update(self):
        self.txt.update()
        self.combo.update()
        self.lbl_mensaje.update()

    def build_inputs(self):
        return self._create_widgets()