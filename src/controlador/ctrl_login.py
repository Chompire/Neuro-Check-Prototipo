from flet_mvc import FletController
import flet as ft
class LoginController(FletController):
    def handle_login_click(self, e):
        self.view.mensaje_error.current.value = ""
        self.page.update()
        rut = self.view.rut_field.current.value
        password = self.view.password_field.current.value
        leer_profesor = self.model.leer_profesor_por_rut_contra_estado(rut, password)
        profesor_cargado = self.model.cargar_profesor(rut, password)
        if profesor_cargado:
            prof_id = self.model.datos_profesor.pro_nameID
            self.model.actualizar_profesor(prof_id, {"pro_online_state": 1})
            self.page.client_storage.set("profesor_id", prof_id)
            if leer_profesor.pro_state == 1:
                if self.model.datos_profesor.pro_cargo == 1:
                    self.page.go("/inicio_pie")
                else:
                    self.page.go("/inicio_profesor")
            else:
                self.show_error_feedback("Cuenta desactivada.")
        else:
            self.show_error_feedback("RUT o contraseña incorrectos.")

    def show_error_feedback(self, message: str):
        self.view.feedback_snackbar.content = ft.Text(message)
        self.view.feedback_snackbar.bgcolor = ft.Colors.RED_700
        self.view.feedback_snackbar.open = True
        self.page.update()

    def formato_rut(self, e: ft.ControlEvent):
        rut_field = e.control
        raw_rut = "".join(filter(lambda char: char.isdigit() or char.upper() == 'K', rut_field.value))
        if not raw_rut:
            return
        body = raw_rut[:-1]
        dv = raw_rut[-1]
        # Formatear el cuerpo con puntos
        if body:
            reversed_body = body[::-1]
            formatted_reversed_body = ".".join(reversed_body[i:i+3] for i in range(0, len(reversed_body), 3))
            formatted_body = formatted_reversed_body[::-1]
            rut_field.value = f"{formatted_body}-{dv}"
        else:
            rut_field.value = dv # Si solo hay un caracter, es el inicio del cuerpo
        self.page.update()