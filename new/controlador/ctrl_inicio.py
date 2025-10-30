from flet_mvc import FletController

class InicioController(FletController):
    def go_realizar_test(self, e):
        self.page.go("/realizar_test")

    def go_perfil_docente(self, e):
        self.page.go("/perfil_docente")