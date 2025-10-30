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
            if self.model.datos_profesor['pro_cargo'] == 1: # 1 para PIE
                self.page.go("/inicio_pie")
            else: # Otro cargo (docente normal)
                self.page.go("/inicio_profesor")
        else:
            self.show_error_snackbar("RUT o contraseña incorrectos.")
            
            # Opcional: Usar SnackBar para una notificación más prominente
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Fallo en la autenticación. Intente de nuevo.", color=ft.colors.WHITE),
                open=True,
                bgcolor=ft.colors.RED_700
            )
            
        # 4. Actualizar la página para que los cambios se muestren
    def show_error_snackbar(self, message: str):
        """Método auxiliar para mostrar mensajes de error en el controlador."""
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            open=True,
            bgcolor=ft.colors.RED_700
        )
        self.page.update()