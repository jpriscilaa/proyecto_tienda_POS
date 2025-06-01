#prueba documentacion lista personalizada
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            width=700,
            bgcolor=ft.Colors.YELLOW,
            border=ft.border.all(2, ft.Colors.RED),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.BLUE),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREEN),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.BLUE,
            heading_row_height=100,
            data_row_color={ft.ControlState.HOVERED: "#0000FF"},
            show_checkbox_column=False,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    ft.Text("Column 1"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Column 2"),
                    tooltip="This is a second column",
                    numeric=True,
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=[
                ft.DataRow(
                    [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow(
                    [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))], 
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}")
                ),
                ft.DataRow(
                    [ft.DataCell(ft.Text("C")), ft.DataCell(ft.Text("3"))], 
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}")
                )
            ],
        ),
    )


ft.app(target=main)