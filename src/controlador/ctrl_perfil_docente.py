from flet_mvc import FletController
import flet as ft
import crud as db
import datetime

class PerfilDocenteController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_test_id = None
        self.res_det_id = None
        self.pro_id = None

    def cargar_datos_docente(self):
        self.view.info_table.rows.clear()
        doc_info = self.model.datos_profesor

        if not doc_info:
            self.view.info_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No se pudieron cargar los datos.", text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ])
            )
            return
        
        row = ft.DataRow(cells=[
            ft.DataCell(ft.Text(f"{doc_info.pro_nombre_1} {doc_info.pro_nombre_2 or ''}".strip())),
            ft.DataCell(ft.Text(f"{doc_info.pro_apellido_pat} {doc_info.pro_apellido_mat}")),
            ft.DataCell(ft.Text(doc_info.pro_rut)),
            ft.DataCell(ft.Text("Profesional PIE" if doc_info.pro_cargo == 1 else "Profesor Docente")),
            ft.DataCell(ft.Text(str(doc_info.num_encuestas) if hasattr(doc_info, 'num_encuestas') else "0")),
        ])
        self.view.info_table.rows.append(row)

        if doc_info.pro_cargo == 1:
            self.cargar_cursos_pie(doc_info.pro_nameID)
            self.view.graficos_container.visible = True
        else:
            self.cargar_cursos_pie(doc_info.pro_nameID)
            self.view.graficos_container.visible = False

        self.page.update()

    def cargar_cursos_pie(self, pro_id):
        self.view.cursos_designados_table.rows.clear()
        resultados_detallados_profesional = self.model.leer_resultados_detallados(pro_ID=pro_id)
        
        conteo_por_curso = {}
        for resultado in resultados_detallados_profesional:
            curso = resultado.lvl_curso
            if curso:
                conteo_por_curso[curso] = conteo_por_curso.get(curso, 0) + 1
        todos_los_cursos = self.model.leer_cursos()
        cursos_map = {c.cur_nombre: c for c in todos_los_cursos}
        for nombre_curso, conteo in conteo_por_curso.items():
            curso_obj = cursos_map.get(nombre_curso)
            año_curso = str(curso_obj.cur_año) if curso_obj else "N/A"
            estado_curso = "Habilitado" if curso_obj and curso_obj.cur_state else "Inhabilitado"
            self.view.cursos_designados_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nombre_curso)),
                    ft.DataCell(ft.Text(año_curso)),
                    ft.DataCell(ft.Text(str(conteo))),
                    ft.DataCell(ft.Text(estado_curso)),
                ])
            )
        self.page.update()

    def cargar_estadisticas_cursos_encuestados(self):   
        current_year_str = str(datetime.datetime.now().year)
        current_year_int = datetime.datetime.now().year
        profesor = self.model.datos_profesor
        resultados_detallados_profesional = self.model.leer_resultados_detallados(pro_ID=profesor.pro_nameID, cur_año=current_year_int)
        todos_los_cursos = self.model.leer_cursos()
        cursos_habilitados = {c.cur_nombre for c in todos_los_cursos if c.cur_state == 1}

        cursos_asignados_nombres = set()
        if profesor.pro_cargo == 1:
            cursos_pie_info = self.model.leer_cursos_pie(profesor.pro_nameID)
            if cursos_pie_info and cursos_pie_info.cursos_a_cargo:
                cursos_asignados_ids = cursos_pie_info.cursos_a_cargo.split(',')
                cursos_asignados_nombres = {c.cur_nombre for c in todos_los_cursos if str(c.cur_nameID) in cursos_asignados_ids and c.cur_state == 1}

        conteo_por_curso = {}
        for resultado in resultados_detallados_profesional:
            curso = resultado.lvl_curso
            if curso in cursos_habilitados:
                conteo_por_curso[curso] = conteo_por_curso.get(curso, 0) + 1

        conteo_por_curso_totales = {}
        cursos_para_totales = cursos_asignados_nombres if profesor.pro_cargo == 1 else conteo_por_curso.keys()
        
        for curso_nombre in cursos_para_totales: (conteo_por_curso_totales.update({curso_nombre: sum(1 for res in self.model.leer_resultados_detallados(lvl_curso=curso_nombre, cur_año=current_year_int) if str(res.cur_año) == current_year_str)}) if curso_nombre in conteo_por_curso else None)
        bar_groups1 = []
        axis_labels1 = []
        bar_groups2 = []
        axis_labels2 = []
        conteo_riesgo_alto_por_curso = {}
        if profesor.pro_cargo == 1 and cursos_asignados_nombres:
            for curso_nombre in cursos_asignados_nombres:
                resultados_totales_curso = self.model.leer_resultados_detallados(lvl_curso=curso_nombre, cur_año=current_year_int)
                conteo_alto_riesgo = sum(1 for res in resultados_totales_curso if res.cur_año == current_year_int and res.det_porcentaje >= 70)
                if conteo_alto_riesgo > 0:
                    conteo_riesgo_alto_por_curso[curso_nombre] = conteo_alto_riesgo

        pie_chart_sections = []
        colors_list = [ft.Colors.RED_700, ft.Colors.ORANGE, ft.Colors.DEEP_ORANGE, ft.Colors.RED_ACCENT]
        for i, (curso, conteo) in enumerate(conteo_riesgo_alto_por_curso.items()):
            pie_chart_sections.append(ft.PieChartSection(
                value=conteo,
                title=f"{curso} ({conteo})",
                title_style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                color=colors_list[i % len(colors_list)],
                radius=200,
            ))

        conteo_riesgo_alto_por_estudiante = {}
        if profesor.pro_cargo == 1:
            for curso_nombre in cursos_asignados_nombres:
                resultados_totales_curso = self.model.leer_resultados_detallados(lvl_curso=curso_nombre, cur_año=current_year_int)
                for res in resultados_totales_curso:
                    if res.det_porcentaje >= 70:
                        nombre_estudiante = f"{res.det_nameES} {res.det_apellidoES}"
                        conteo_riesgo_alto_por_estudiante[nombre_estudiante] = conteo_riesgo_alto_por_estudiante.get(nombre_estudiante, 0) + 1
        
        pie_chart_estudiantes_sections = []
        if profesor.pro_cargo == 1:
            colors_list_estudiantes = [ft.Colors.BLUE_700, ft.Colors.LIGHT_BLUE, ft.Colors.CYAN, ft.Colors.TEAL]
            for i, (estudiante, conteo) in enumerate(conteo_riesgo_alto_por_estudiante.items()):
                pie_chart_estudiantes_sections.append(ft.PieChartSection(
                    value=conteo,
                    title=f"{estudiante} ({conteo})",
                    title_style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    color=colors_list_estudiantes[i % len(colors_list_estudiantes)],
                    radius=200,
                ))

        for i, (curso, conteo) in enumerate(conteo_por_curso.items()):
            bar_groups1.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=conteo,
                            width=30,
                            color=ft.Colors.BLUE,
                            tooltip=f"{conteo} encuestas",
                            border_radius=4,
                        ),
                    ],
                )
            )
            axis_labels1.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(curso, size=10, weight=ft.FontWeight.BOLD, color="black"),
                )
            )
        for i, (curso, conteo) in enumerate(conteo_por_curso_totales.items()):
            bar_groups2.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=conteo,
                            width=30,
                            color=ft.Colors.GREEN,
                            tooltip=f"{conteo} encuestas",
                            border_radius=4,
                        ),
                    ],
                )
            )
            axis_labels2.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(curso, size=10, weight=ft.FontWeight.BOLD, color="black"),
                )
            )


        self.view.stat_cantidad_cursos_encuestados.bar_groups = bar_groups1
        self.view.stat_cantidad_cursos_encuestados.bottom_axis.labels = axis_labels1
        self.view.stat_cantidad_cursos_encuestados_totales.bar_groups = bar_groups2
        self.view.stat_cantidad_cursos_encuestados_totales.bottom_axis.labels = axis_labels2

        self.view.cursos_en_rojo.sections = pie_chart_sections
        self.view.estudiantes_rojos.sections = pie_chart_estudiantes_sections

        self.page.update()

    def cargar_estadisticas_cursos_rojos(self):
        if not self.model.datos_profesor:
            return

        pro_id = self.model.datos_profesor.pro_nameID
        resultados_profesional = self.model.leer_resultados_detallados(pro_ID=pro_id)

        conteo_rojos_por_curso = {}
        for resultado in resultados_profesional:
            if resultado.det_porcentaje < 50:
                curso = resultado.lvl_curso
                if curso:
                    conteo_rojos_por_curso[curso] = conteo_rojos_por_curso.get(curso, 0) + 1

        bar_groups = []
        axis_labels = []
        for i, (curso, conteo) in enumerate(conteo_rojos_por_curso.items()):
            bar_groups.append(ft.BarChartGroup(
                x=i,
                bar_rods=[ft.BarChartRod(
                    from_y=0, to_y=conteo, width=30, color=ft.Colors.RED,
                    tooltip=f"{conteo} resultados bajos", border_radius=4
                )]
            ))
            axis_labels.append(ft.ChartAxisLabel(
                value=i, label=ft.Text(curso, size=10, weight=ft.FontWeight.BOLD, color="black")
            ))

        self.view.stat_cursos_rojos.bar_groups = bar_groups
        self.view.stat_cursos_rojos.bottom_axis.labels = axis_labels
        self.page.update()