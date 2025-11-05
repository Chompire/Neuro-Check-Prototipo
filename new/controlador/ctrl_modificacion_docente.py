from flet_mvc import FletController
import flet as ft
import re
from datetime import datetime

class ModificacionDocenteController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_prof_id = None
        self.password_define = "neurocheck2025"
        self.selected_course_id = None

    def load_profesores_to_table(self, id_to_select=None):
        self.view.data_table.rows.clear()
        profesores = self.model.leer_profesores()
        if profesores:
            for prof in profesores:
                self.view.data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"{prof.pro_nombre_1} {prof.pro_nombre_2 or ''}".strip())),
                            ft.DataCell(ft.Text(f"{prof.pro_apellido_pat} {prof.pro_apellido_mat}")),
                            ft.DataCell(ft.Text(prof.pro_rut)),
                            ft.DataCell(ft.Text("Profesional PIE" if prof.pro_cargo else "Docente")),
                            ft.DataCell(ft.Text(prof.cur_nombre or "N/A")),
                            ft.DataCell(ft.Text("Habilitado" if prof.pro_state else "Inhabilitado")),
                        ],
                        data=prof,
                        selected=True if id_to_select is not None and prof.pro_nameID == id_to_select else False,
                        on_select_changed=self.on_row_select,
                    )
                )
        self.page.update()

    def load_cursos_to_table(self, id_to_select=None):
        self.view.course_data_table.rows.clear()
        cursos = self.model.leer_cursos()
        if cursos:
            for curso in cursos:
                self.view.course_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(curso.cur_nombre)),
                            ft.DataCell(ft.Text(str(curso.cur_año))),
                            ft.DataCell(ft.Text("Habilitado" if curso.cur_state else "Inhabilitado")),
                        ],
                        data=curso,
                        selected=True if id_to_select is not None and curso.cur_nameID == id_to_select else False,
                        on_select_changed=self.on_course_row_select,
                    )
                )

    def on_row_select(self, e):
        selected_prof = e.control.data
        is_currently_selected = e.control.selected

        for row in self.view.data_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.view.edit_button.visible = True
            self.view.delete_button.visible = True
            self.view.add_button.disabled = True
            self.selected_prof_id = selected_prof.pro_nameID
            
            self.view.nombre1.value = selected_prof.pro_nombre_1 or ""
            self.view.nombre2.value = selected_prof.pro_nombre_2 or ""
            self.view.nombre3.value = selected_prof.pro_nombre_3 or ""
            self.view.apellido_pat.value = selected_prof.pro_apellido_pat or ""
            self.view.apellido_mat.value = selected_prof.pro_apellido_mat or ""
            self.view.rut_field.value = selected_prof.pro_rut or ""
            self.view.cargo_field.value = "Profesional PIE" if selected_prof.pro_cargo else "Docente"
            self.view.curso_field.value = selected_prof.lvl_curso
            self.view.estado_field.value = "Habilitado" if selected_prof.pro_state else "Inhabilitado"
        else:
            self.clear_form_fields()
            self.reset_selection_state()
        self.page.update()

    def clear_form_fields(self):
        self.view.nombre1.value = ""
        self.view.nombre2.value = ""
        self.view.nombre3.value = ""
        self.view.apellido_pat.value = ""
        self.view.apellido_mat.value = ""
        self.view.rut_field.value = ""
        self.view.cargo_field.value = None
        self.view.curso_field.value = None
        self.view.estado_field.value = None

    def on_course_row_select(self, e):
        selected_course = e.control.data
        is_currently_selected = e.control.selected

        for row in self.view.course_data_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.view.update_course_button.visible = True
            self.selected_course_id = selected_course.cur_nameID

            self.view.course_name_field.value = selected_course.cur_nombre
            self.view.course_year_field.value = str(selected_course.cur_año)
            self.view.course_state_field.value = "Habilitado" if selected_course.cur_state else "Inhabilitado"
        else:
            for row in self.view.course_data_table.rows:
                row.selected = False
                self.view.course_name_field.value = ""
                self.view.course_year_field.value = ""
                self.view.course_state_field.value = None
                self.view.update_course_button.visible = False
                self.selected_course_id = None
                
        self.page.update()


    def reset_selection_state(self):
        for row in self.view.data_table.rows:
            row.selected = False
        
        self.view.edit_button.visible = False
        self.view.delete_button.visible = False
        self.view.add_button.disabled = False
        self.selected_prof_id = None

    def add_profesor(self, e):
        rut = self.view.rut_field.value.strip()
        if not self.validar_rut(rut):
            self.view.show_feedback("Error: El RUT ingresado no es válido.", ft.colors.RED)
            return

        if self.model.leer_profesor_por_rut(rut):
            self.view.show_feedback("Error: El RUT ya está registrado.", ft.colors.RED)
            return

        cargo_valor = 1 if self.view.cargo_field.value == "Profesional PIE" else 0
        estado_valor = 1 if self.view.estado_field.value == "Habilitado" else 0
        
        datos_nuevos = (
            self.view.nombre1.value, self.view.nombre2.value, self.view.nombre3.value,
            self.view.apellido_pat.value, self.view.apellido_mat.value,
            rut,
            cargo_valor, self.password_define, 
            self.view.curso_field.value, estado_valor, None
        )

        if self.model.crear_profesor(datos_nuevos):
            self.view.show_feedback("Profesor agregado con éxito.", ft.colors.GREEN)
            self.load_profesores_to_table()
            self.clear_form_fields()
            self.reset_selection_state()
        else:
            self.view.show_feedback("Error al agregar profesor.", ft.colors.RED)
        self.close_dialog(e, 'add')

    def update_profesor(self, e):
        if self.selected_prof_id is None: return

        rut = self.view.rut_field.value.strip()
        if not self.validar_rut(rut):
            self.view.show_feedback("Error: El RUT ingresado no es válido.", ft.colors.RED)
            return

        estado_valor = 1 if self.view.estado_field.value == "Habilitado" else 0
        cargo_valor = 1 if self.view.cargo_field.value == "Profesional PIE" else 0
        datos_actualizados = {
            "pro_nombre_1": self.view.nombre1.value, "pro_nombre_2": self.view.nombre2.value, "pro_nombre_3": self.view.nombre3.value,
            "pro_apellido_pat": self.view.apellido_pat.value, "pro_apellido_mat": self.view.apellido_mat.value,
            "pro_rut": self.view.rut_field.value,
            "pro_cargo": cargo_valor, "lvl_curso": self.view.curso_field.value, "pro_state": estado_valor,
        }
        self.model.actualizar_profesor(self.selected_prof_id, datos_actualizados)
        self.view.show_feedback("Profesor actualizado con éxito.", ft.colors.GREEN)
        self.load_profesores_to_table(id_to_select=self.selected_prof_id)
        self.close_dialog(e, 'edit')

    def update_curso(self, e):
        if self.selected_course_id is None: return

        nuevo_estado_str = self.view.course_state_field.value
        nuevo_estado_val = 1 if nuevo_estado_str == "Habilitado" else 0

        datos_actualizados = {"cur_state": nuevo_estado_val}
        self.model.actualizar_curso(self.selected_course_id, datos_actualizados)

        # Lógica para crear el siguiente curso si se inhabilita
        if nuevo_estado_val == 0:
            nombre_curso_actual = self.view.course_name_field.value
            match = re.search(r'\d+', nombre_curso_actual)
            if match:
                nivel_actual = int(match.group())
                siguiente_nivel = nivel_actual + 1
                nombre_siguiente_curso = nombre_curso_actual.replace(str(nivel_actual), str(siguiente_nivel), 1)
                año_actual = datetime.now().year

                self.model.crear_curso(nombre_siguiente_curso, año_actual)
                self.view.show_feedback(f"Curso '{nombre_siguiente_curso}' para el {año_actual} creado.", ft.colors.BLUE)

        self.view.show_feedback("Estado del curso actualizado.", ft.colors.GREEN)
        self.load_cursos_to_table(id_to_select=self.selected_course_id)
        self.view.curso_field.options = self.lista_cursos()
        self.page.update()

    def open_course_dialog(self, e):
        self.load_cursos_to_table()
        self.view.course_dialog.open = True
        self.page.update()

    def close_course_dialog(self, e):
        self.view.course_dialog.open = False
        self.page.update()

    def delete_profesor(self, e):
        if self.selected_prof_id:
            self.model.eliminar_profesor(self.selected_prof_id)
            self.view.show_feedback("Profesor eliminado con éxito.", ft.colors.GREEN)
            self.load_profesores_to_table()
            self.clear_form_fields()
            self.reset_selection_state()
        self.close_dialog(e, 'delete')

    def open_dialog(self, e, tipo: str):
        dialog = getattr(self.view, f"{tipo}_dialog")
        dialog.open = True
        self.page.update()

    def close_dialog(self, e, tipo: str):
        dialog = getattr(self.view, f"{tipo}_dialog")
        dialog.open = False
        self.page.update()

    def lista_cursos(self):
        cursos = self.model.leer_cursos()
        if cursos:
            return [ft.dropdown.Option(key=curso.cur_nameID, text=curso.cur_nombre) for curso in cursos]
        return []

    def formato_rut(self, e: ft.ControlEvent):
        """Formatea automáticamente el RUT en el TextField mientras el usuario escribe."""
        rut_field = e.control
        # Limpiar el RUT de caracteres no deseados
        raw_rut = "".join(filter(lambda char: char.isdigit() or char.upper() == 'K', rut_field.value))
        if not raw_rut:
            return
        # Separar cuerpo y dígito verificador
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

    @staticmethod
    def validar_rut(rut: str) -> bool:
        rut = rut.upper().replace(".", "").replace("-", "")
        if not rut[:-1].isdigit() or not (rut[-1].isdigit() or rut[-1] == 'K'):
            return False
        
        numero = rut[:-1]
        dv = rut[-1]
        
        try:
            reversed_numero = numero[::-1]
            multiplicador = 2
            suma = 0
            for d in reversed_numero:
                suma += int(d) * multiplicador
                multiplicador += 1
                if multiplicador == 8:
                    multiplicador = 2
            
            resto = suma % 11
            dv_calculado = 11 - resto
            
            if dv_calculado == 11:
                dv_esperado = '0'
            elif dv_calculado == 10:
                dv_esperado = 'K'
            else:
                dv_esperado = str(dv_calculado)
                
            return dv == dv_esperado
        except Exception:
            return False