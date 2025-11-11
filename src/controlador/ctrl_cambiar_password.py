from flet_mvc import FletController
import flet as ft

class CambiarPasswordController(FletController):
    def cambiar_contrasena(self, e):
        nueva_contrasena = self.view.nuevo_password.value
        confirmar_contrasena = self.view.confirmar_password.value