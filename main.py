from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from inventory_ui import build_inventory_ui
from kivy.core.window import Window
from kivy.clock import Clock
from save import save_csv
from excel import save_to_excel
from manual_mode import add_to_temp_list as manual_add_to_temp_list
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import platform
import json
import os
from datetime import datetime

class InventoryApp(App):
    def build(self):
        self.title = "Склад Таврово-2, Белгород"
        self.autosave_every = 500
        self.autosave_counter = 0
        self.autosave_base_name = None

        # Загрузка базы new.json
        try:
            with open("new.json", "r", encoding="utf-8") as f:
                self.new_items = json.load(f)
        except:
            self.new_items = []

        return build_inventory_ui(self)

    def set_mode(self, mode):
        self.mode = mode
        self.label.text = f"[b]Режим: {'Потоковый' if mode == 'auto' else 'Ручной'}[/b]"

    def find_product(self, barcode):
        barcode = str(barcode).strip()

        def match(code):
            if isinstance(code, list):
                return barcode in [str(c).strip() for c in code]
            return str(code).strip() == barcode

        for item in self.sadopt:
            if match(item.get("Штрихкод")):
                return item
        for item in self.region:
            if match(item.get("Штрихкод")):
                return item
        for item in self.new_items:
            if match(item.get("Штрихкод")):
                return item
        return None

    def process_barcode(self):
        barcode = self.barcode_input.text.strip()
        if not barcode:
            return

        item = self.find_product(barcode)
        if item:
            name = item.get("Название", "Без названия")
            self.qty_input.text = "1"
            self.product_name_input.text = name
            self.current_item = item

            if self.mode == "auto":
                self.add_to_temp_list()
        else:
            self.label.text = "[color=ff0000][b]Товар не найден[/b][/color]"
            self.product_name_input.text = ""
            self.current_item = {}

            # Звук на Android
            if platform == "android":
                try:
                    from jnius import autoclass
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    MediaPlayer = autoclass('android.media.MediaPlayer')
                    Uri = autoclass('android.net.Uri')
                    sound = MediaPlayer.create(
                        PythonActivity.mActivity,
                        Uri.parse("file:///sdcard/Download/beep.mp3")
                    )
                    sound.start()
                except Exception as e:
                    print("Звук ошибки не проигрался:", e)

            self.show_manual_entry_popup(barcode)

        # 🟩 Вернуть курсор в поле Штрихкод
        Clock.schedule_once(lambda dt: setattr(self.barcode_input, 'focus', True), 0.05)

    def show_manual_entry_popup(self, barcode):
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        input_name = TextInput(hint_text="Введите название товара", multiline=False)
        box.add_widget(input_name)

        def add_manual_item(instance):
            name = input_name.text.strip()
            if name:
                self.qty_input.text = "1"
                self.product_name_input.text = name
                self.current_item = {
                    "Артикул": "MANUAL",
                    "Название": name,
                    "Количество": "1",
                    "Штрихкод": barcode
                }

                # Добавляем в список
                self.add_to_temp_list()
                self.popup.dismiss()

                # Сохраняем в new.json
                new_entry = {
                    "Артикул": "MANUAL",
                    "Название": name,
                    "Штрихкод": barcode
                }

                try:
                    path = "new.json"
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                    else:
                        data = []

                    # Проверим, чтобы не было дублей
                    if not any(str(item.get("Штрихкод")) == str(barcode) for item in data):
                        data.append(new_entry)
                        with open(path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)

                        self.new_items.append(new_entry)

                except Exception as e:
                    print("Ошибка при записи в new.json:", e)
            else:
                input_name.hint_text = "Название обязательно!"

        btn = Button(text="Добавить")
        btn.bind(on_press=add_manual_item)
        box.add_widget(btn)

        self.popup = Popup(title="Товар не найден", content=box, size_hint=(0.8, 0.4))
        self.popup.open()

    def add_to_temp_list(self):
        if self.mode == "auto":
            qty = self.qty_input.text.strip()
            employee = self.employee_input.text.strip()
            self.barcode_input.text = ""

            if not self.current_item or not qty or not employee:
                self.label.text = "Укажите имя и количество"
                return

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                "Артикул": self.current_item.get("Артикул", ""),
                "Название": self.current_item.get("Название", ""),
                "Количество": qty,
                "Штрихкод": self.current_item.get("Штрихкод", ""),
                "Сотрудник": employee,
                "Время": timestamp
            }

            self.data.append(entry)
            self.label.text = f"[b]Добавлено:[/b] {entry['Название']} x{qty}"
            self.qty_input.text = ""
            self.current_item = {}

            Clock.schedule_once(lambda dt: setattr(self.barcode_input, 'focus', True), 0.05)

            if len(self.data) % self.autosave_every == 0:
                self.autosave_counter += 1
                if self.autosave_base_name is None:
                    self.autosave_base_name = f"invent_{employee}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
                filename = f"{self.autosave_base_name}-{self.autosave_counter}.xlsx"
                save_to_excel(self.data, employee, filename)
                self.label.text += f"\nАвтосохранение: {filename}"
        else:
            manual_add_to_temp_list(self)

if __name__ == "__main__":
    InventoryApp().run()
