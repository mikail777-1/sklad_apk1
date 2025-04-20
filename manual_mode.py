from datetime import datetime
from excel import save_to_excel

def add_to_temp_list(app):
    qty = app.qty_input.text.strip()
    employee = app.employee_input.text.strip()
    barcode = app.barcode_input.text.strip()

    if not barcode:
        app.label.text = "Введите или отсканируйте штрихкод"
        return
    if not qty or not employee:
        app.label.text = "Укажите количество и имя"
        return

    item = app.find_product(barcode)
    if not item:
        app.label.text = "Товар не найден"
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "Артикул": item.get("Артикул", ""),
        "Название": item.get("Название", ""),
        "Количество": qty,
        "Штрихкод": barcode,
        "Сотрудник": employee,
        "Время": timestamp
    }

    app.data.append(entry)
    app.label.text = f"[b]Добавлено:[/b] {entry['Название']} x{qty}"
    app.qty_input.text = ""
    app.product_name_input.text = item.get("Название", "")
    app.current_item = {}

    if len(app.data) % app.autosave_every == 0:
        app.autosave_counter += 1
        if app.autosave_base_name is None:
            app.autosave_base_name = f"invent_{employee}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        filename = f"{app.autosave_base_name}-{app.autosave_counter}.xlsx"
        save_to_excel(app.data, employee, filename)
        app.label.text += f"\nАвтосохранение: {filename}"
