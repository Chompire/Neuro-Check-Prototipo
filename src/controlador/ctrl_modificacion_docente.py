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
        self.online_state = False
        self.numpage_prof = 5
        self.numpage_cursos = 5
        self.current_page_prof = 0
        self.current_page_cursos = 0
        self.total_page_prof = 1
        self.total_page_cursos = 1

    def initialize_view(self):
        cursos = self.model.leer_cursos()
        self.build_cursos_checkboxes(cursos)

    def load_profesores_to_table(self, id_to_select=None, profesores_a_mostrar = None):
        self.view.data_table.rows.clear()
        if profesores_a_mostrar is None:
            profesores_a_mostrar = self.model.leer_profesores()
        total_items_pro = len(profesores_a_mostrar)
        total_pages_pro = (total_items_pro + self.numpage_prof - 1) // self.numpage_prof
        if total_pages_pro == 0: total_pages_pro = 1
        start_index = self.current_page_prof * self.numpage_prof
        end_index = start_index + self.numpage_prof
        profesores_pagina_actual = profesores_a_mostrar[start_index:end_index]
        self.view.page_label_pro.value = f"Página {self.current_page_prof + 1} de {total_pages_pro}"
        self.view.prev_button_pro.visible = self.current_page_prof > 0
        self.view.next_button_pro.visible = self.current_page_prof < total_pages_pro - 1
        self.total_page_prof = total_pages_pro
        if profesores_a_mostrar:
            for prof in profesores_pagina_actual:
                    self.view.data_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{prof.pro_nombre_1} {prof.pro_nombre_2 or ''}".strip())),
                                ft.DataCell(ft.Text(f"{prof.pro_apellido_pat} {prof.pro_apellido_mat}")),
                                ft.DataCell(ft.Text(prof.pro_rut)),
                                ft.DataCell(ft.Text("Profesional PIE" if prof.pro_cargo else "Docente")),
                                ft.DataCell(ft.Text("N/A")), # Ya no se muestra el curso
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
        cursos_totales = self.model.leer_cursos()
        if cursos_totales:
            total_items_cursos = len(cursos_totales)
            total_pages_cursos = (total_items_cursos + self.numpage_cursos - 1) // self.numpage_cursos
            if total_pages_cursos == 0: total_pages_cursos = 1
            
            start_index = self.current_page_cursos * self.numpage_cursos
            end_index = start_index + self.numpage_cursos
            cursos_pagina_actual = cursos_totales[start_index:end_index]

            self.view.page_label_cursos.value = f"Página {self.current_page_cursos + 1} de {total_pages_cursos}"
            self.view.prev_button_cursos.visible = self.current_page_cursos > 0
            self.view.next_button_cursos.visible = self.current_page_cursos < total_pages_cursos - 1

            for curso in cursos_pagina_actual:
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
        self.page.update()

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
            self.view.estado_field.value = "Habilitado" if selected_prof.pro_state else "Inhabilitado"

            # Lógica para mostrar y marcar los cursos si es PIE
            if selected_prof.pro_cargo == 1:
                self.view.cursos_checkbox_group.visible = True
                cursos_asignados_raw = self.model.leer_cursos_pie(self.selected_prof_id)
                cursos_asignados_ids = cursos_asignados_raw[0].split(',') if cursos_asignados_raw and cursos_asignados_raw[0] else []
                # Iterar solo sobre los checkboxes, omitiendo el título (que es el primer control)
                for checkbox in self.view.cursos_checkbox_group.content.controls[1:]:
                    checkbox.value = str(checkbox.data) in cursos_asignados_ids if isinstance(checkbox, ft.Checkbox) else checkbox.value
            else:
                self.view.cursos_checkbox_group.visible = False

        else:
            self.clear_form_fields()
            self.reset_selection_state()
        self.page.update()

    def next_page_pro(self, e):
        prof = self.model.leer_profesores()
        total_items = len(prof)
        total_pages = (total_items + self.numpage_prof - 1) // self.numpage_prof
        if self.current_page_prof < total_pages - 1:
            self.current_page_prof += 1
            self.load_profesores_to_table()

    def prev_page_pro(self, e):
        if self.current_page_prof > 0:
            self.current_page_prof -= 1
            self.load_profesores_to_table()

    def next_page_cursos(self, e):
        cursos_totales = self.model.leer_cursos()
        total_items = len(cursos_totales)
        total_pages = (total_items + self.numpage_cursos - 1) // self.numpage_cursos
        if self.current_page_cursos < total_pages - 1:
            self.current_page_cursos += 1
            self.load_cursos_to_table()

    def prev_page_cursos(self, e):
        if self.current_page_cursos > 0:
            self.current_page_cursos -= 1
            self.load_cursos_to_table()




    def clear_form_fields(self):
        self.view.nombre1.value = ""
        self.view.nombre2.value = ""
        self.view.nombre3.value = ""
        self.view.apellido_pat.value = ""
        self.view.apellido_mat.value = ""
        self.view.rut_field.value = ""
        self.view.cargo_field.value = None
        self.view.estado_field.value = None
        self.view.cursos_checkbox_group.visible = False
        for checkbox in self.view.cursos_checkbox_group.content.controls:
            checkbox.value = False

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

    def show_feedback(self, message: str, color: str):
        self.view.feedback_snackbar.content = ft.Text(message)
        self.view.feedback_snackbar.bgcolor = color
        self.view.feedback_snackbar.open = True
        self.page.update()

    def build_cursos_checkboxes(self, cursos):
        if len(self.view.cursos_checkbox_group.content.controls) > 1:
            self.view.cursos_checkbox_group.content.controls = [self.view.cursos_checkbox_group.content.controls[0]]

        if cursos:
            # Filtrar solo los cursos que están habilitados (cur_state == 1)
            cursos_habilitados = [curso for curso in cursos if curso.cur_state]
            for curso in cursos_habilitados:
                self.view.cursos_checkbox_group.content.controls.append(
                    ft.Checkbox(
                        label=curso.cur_nombre,
                        data=curso.cur_nameID,
                        check_color=ft.Colors.RED,
                        label_style=ft.TextStyle(color="black")
                    )
                )

    def show_feedback(self, message: str, color: str):
        self.view.feedback_snackbar.content = ft.Text(message)
        self.view.feedback_snackbar.bgcolor = color
        self.view.feedback_snackbar.open = True
        self.page.update()

    def reset_selection_state(self):
        for row in self.view.data_table.rows:
            row.selected = False        
        self.view.edit_button.visible = False
        self.view.delete_button.visible = False
        self.view.add_button.disabled = False
        self.selected_prof_id = None

    def toggle_cursos_visibility(self, e):
        self.view.cursos_checkbox_group.visible = (e.control.value == "Profesional PIE")
        self.page.update()

    def add_profesor(self, e):
        rut = self.view.rut_field.value.strip()
        if not self.validar_rut(rut):
            self.show_feedback("Error: El RUT ingresado no es válido.", ft.Colors.RED)
            return

        if self.model.leer_profesor_por_rut(rut):
            self.show_feedback("Error: El RUT ya está registrado.", ft.Colors.RED)
            return

        cargo_valor = 1 if self.view.cargo_field.value == "Profesional PIE" else 0
        estado_valor = 1 if self.view.estado_field.value == "Habilitado" else 0
        
        datos_nuevos = (
            self.view.nombre1.value, self.view.nombre2.value, self.view.nombre3.value,
            self.view.apellido_pat.value, self.view.apellido_mat.value,
            rut,
            cargo_valor, self.password_define,
            estado_valor, None,
            self.online_state,
        )
        success = self.model.crear_profesor(datos_nuevos)
        if success:
            # Si es PIE, guardar los cursos asignados
            if cargo_valor == 1:
                new_prof = self.model.leer_profesor_por_rut(rut) # Obtenemos el profesor recién creado para su ID
                cursos_seleccionados = [
                    str(cb.data) for cb in self.view.cursos_checkbox_group.content.controls if cb.value
                ]
                cursos_str = ",".join(cursos_seleccionados)
                self.model.crear_asignacion_pie(new_prof.pro_nameID, cursos_str)

            self.show_feedback("Profesor agregado con éxito.", ft.Colors.GREEN)
            self.load_profesores_to_table()
            self.clear_form_fields()
            self.reset_selection_state()
        else:
            self.show_feedback("Error al agregar profesor.", ft.Colors.RED)
        
        self.close_dialog(e, 'add')

    def update_profesor(self, e):
        if self.selected_prof_id is None: return

        rut = self.view.rut_field.value.strip()
        if not self.validar_rut(rut):
            self.show_feedback("Error: El RUT ingresado no es válido.", ft.Colors.RED)
            return

        estado_valor = 1 if self.view.estado_field.value == "Habilitado" else 0
        cargo_valor = 1 if self.view.cargo_field.value == "Profesional PIE" else 0
        datos_actualizados = {
            "pro_nombre_1": self.view.nombre1.value, "pro_nombre_2": self.view.nombre2.value, "pro_nombre_3": self.view.nombre3.value,
            "pro_apellido_pat": self.view.apellido_pat.value, "pro_apellido_mat": self.view.apellido_mat.value,
            "pro_rut": self.view.rut_field.value,
            "pro_cargo": cargo_valor, "pro_state": estado_valor,
        }
        self.model.actualizar_profesor(self.selected_prof_id, datos_actualizados)

        # Actualizar cursos para PIE
        if cargo_valor == 1:
            cursos_seleccionados = [
                str(cb.data) for cb in self.view.cursos_checkbox_group.content.controls if cb.value
            ]
            cursos_str = ",".join(cursos_seleccionados)
            self.model.actualizar_asignacion_pie(self.selected_prof_id, cursos_str)
        else:
            # Si el cargo cambia de PIE a otro, eliminamos la asignación de cursos
            self.model.eliminar_asignacion_pie(self.selected_prof_id)


        self.show_feedback("Profesor actualizado con éxito.", ft.Colors.GREEN)
        self.load_profesores_to_table(id_to_select=self.selected_prof_id)
        self.close_dialog(e, 'edit')

    def update_curso(self, e):
        if self.selected_course_id is None: return

        nuevo_estado_str = self.view.course_state_field.value
        nuevo_estado_val = 1 if nuevo_estado_str == "Habilitado" else 0

        datos_actualizados = {"cur_state": nuevo_estado_val}
        self.model.actualizar_curso(self.selected_course_id, datos_actualizados)
        if nuevo_estado_val == 0:
            nombre_curso_actual = self.view.course_name_field.value
            match = re.search(r'\d+', nombre_curso_actual)
            if match:
                nivel_actual = int(match.group())
                siguiente_nivel = nivel_actual + 1
                nombre_siguiente_curso = nombre_curso_actual.replace(str(nivel_actual), str(siguiente_nivel), 1)
                año_actual = datetime.now().year

                self.model.crear_curso(nombre_siguiente_curso, año_actual)
                self.show_feedback(f"Curso '{nombre_siguiente_curso}' para el {año_actual} creado.", ft.Colors.BLUE)

        self.show_feedback("Estado del curso actualizado.", ft.Colors.GREEN)
        self.load_cursos_to_table(id_to_select=self.selected_course_id)
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
            # También eliminar de la tabla Prof_PIE si existe
            self.model.eliminar_asignacion_pie(self.selected_prof_id)

            self.model.eliminar_profesor(self.selected_prof_id)
            self.show_feedback("Profesor eliminado con éxito.", ft.Colors.GREEN)
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