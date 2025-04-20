from excel import save_to_excel

def save_csv(app, instance=None):
    if not app.data:
        app.label.text = "Нет данных для сохранения"
        return

    employee = app.employee_input.text.strip()
    if not employee:
        app.label.text = "Укажите имя сотрудника перед сохранением"
        return

    save_to_excel(app.data, employee)
    app.label.text = f"[b]Сохранено {len(app.data)} позиций[/b]"
    app.data = []
