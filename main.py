
import flet as ft 
from db import main_db


def main(page: ft.Page):
    page.title = 'todo list'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column(spacing=15) 

    filter_type = 'all'

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_task(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, completed=completed))
        page.update()

    def create_task_row(task_id, task_text, completed):

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id=task_id, is_completed=e.control.value))

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
        
        def deleted_tasks(_):
            main_db.delete_task(task_id)
            load_task()

        deleted_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=deleted_tasks)

        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)

        task_field = ft.TextField(value=task_text, read_only=True, expand=True, on_submit=save_task)

        return ft.Row([checkbox, task_field, edit_button, save_button, deleted_button])
    
    def toggle_task(task_id, is_completed):
        print(f"{task_id} - {is_completed}")
        print(f"{task_id} - {int(is_completed)}")
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_task()

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completed=None))
            print(f'Запись сохранена! ID задачи - {task_id}')
            task_input.value = None
            page.update()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()


    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX, icon_color=ft.Colors.YELLOW),
        ft.ElevatedButton('В ожидании...', on_click=lambda e: set_filter('uncompleted'), icon=ft.Icons.WATCH_LATER, icon_color=ft.Colors.ORANGE),
        ft.ElevatedButton('Готово', on_click=lambda e: set_filter('completed'), icon=ft.Icons.CHECK_BOX, icon_color=ft.Colors.GREEN)
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    task_input = ft.TextField(label='Введите задачу', expand=True, on_submit=add_task)
    task_input_button = ft.IconButton(icon=ft.Icons.SEND, on_click=add_task)

    main_objects = ft.Row([task_input, task_input_button])

    page.add(main_objects, filter_buttons, task_list)
    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)