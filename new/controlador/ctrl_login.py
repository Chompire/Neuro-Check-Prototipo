from flet_mvc import FletController
import flet as ft
class LoginController(FletController):
    def handle_login_click(self, e):
        self.view.mensaje_error.current.value = ""
        self.page.update()
        rut = self.view.rut_field.current.value
        password = self.view.password_field.current.value
        profesor_cargado = self.model.cargar_profesor(rut, password)
        if profesor_cargado:
            # Verificar el cargo del profesor
            if self.model.datos_profesor.pro_cargo == 1: # 1 para PIE
                self.page.go("/inicio_pie")
            else: # Otro cargo (docente normal)
                self.page.go("/inicio_profesor")
        else:
            self.show_error_feedback("RUT o contraseña incorrectos.")

    def show_error_feedback(self, message: str):
        self.view.feedback_snackbar.content = ft.Text(message)
        self.view.feedback_snackbar.bgcolor = ft.colors.RED_700
        self.view.feedback_snackbar.open = True
        self.page.update()