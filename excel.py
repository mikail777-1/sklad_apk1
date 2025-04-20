from openpyxl import Workbook
from datetime import datetime
from collections import defaultdict

def save_to_excel(data, employee, filename=None):
    if filename is None:
        filename = f"invent_{employee}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"

    # 🔁 Группируем по (Артикул, Штрихкод)
    grouped = defaultdict(lambda: {
        "Артикул": "",
        "Название": "",
        "Количество": 0,
        "Штрихкод": "",
        "Сотрудник": employee,
        "Время": ""
    })

    for item in data:
        # ✅ Универсальный штрихкод (строка)
        barcode = item.get("Штрихкод", "")
        if isinstance(barcode, list):
            barcode = barcode[0] if barcode else ""
        barcode = str(barcode)

        key = (item.get("Артикул", ""), barcode)

        grouped[key]["Артикул"] = item.get("Артикул", "")
        grouped[key]["Название"] = item.get("Название", "")
        grouped[key]["Количество"] += int(item.get("Количество", 0))
        grouped[key]["Штрихкод"] = barcode
        grouped[key]["Сотрудник"] = item.get("Сотрудник", employee)
        grouped[key]["Время"] = item.get("Время", "")

    wb = Workbook()
    ws = wb.active
    ws.title = "Инвентаризация"

    headers = ["Артикул", "Название", "Количество", "Штрихкод", "Сотрудник", "Время"]
    ws.append(headers)

    for group in grouped.values():
        ws.append([
            group["Артикул"],
            group["Название"],
            group["Количество"],
            group["Штрихкод"],
            group["Сотрудник"],
            group["Время"]
        ])

    wb.save(filename)
    print(f"Файл сохранён: {filename}")
