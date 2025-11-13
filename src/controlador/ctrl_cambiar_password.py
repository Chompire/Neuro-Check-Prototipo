from flet_mvc import FletController
import flet as ft

class CambiarPasswordController(FletController):
    def cambiar_contrasena(self, e):
        nueva_contrasena = self.view.nuevo_password.value
        confirmar_contrasena = self.view.confirmar_password.value

        if not nueva_contrasena or not confirmar_contrasena:
            self.show_feedback("Ambos campos son obligatorios.", ft.Colors.RED)
            return

        if nueva_contrasena != confirmar_contrasena:
            self.show_feedback("Las contraseñas no coinciden.", ft.Colors.RED)
            return
        
        prof_id = self.model.datos_profesor.pro_nameID
        datos_actualizados = {"pro_password": nueva_contrasena}
        
        self.model.actualizar_profesor(prof_id, datos_actualizados)
        
        self.show_feedback("Contraseña actualizada con éxito.", ft.Colors.GREEN)
        self.view.nuevo_password.value = ""
        self.view.confirmar_password.value = ""
        self.page.update()

    def show_feedback(self, message: str, color: str):
        self.view.feedback_snackbar.content = ft.Text(message)
        self.view.feedback_snackbar.bgcolor = color
        self.view.feedback_snackbar.open = True
        self.page.update()