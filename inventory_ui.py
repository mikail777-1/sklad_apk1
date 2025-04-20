import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp, sp
from kivy.core.window import Window
from save import save_csv
from embedded_data import get_sadopt_items, get_region_items  # 📌 Добавлено

def build_inventory_ui(app):
    app.data = []
    app.current_item = {}
    app.mode = "auto"
    app.sadopt = []
    app.region = []
    app._barcode_timer = None

    Window.clearcolor = (1, 1, 1, 1)

    layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

    # 🟩 Название товара (вверху)
    app.product_name_input = TextInput(
        hint_text="Название",
        multiline=True,
        readonly=True,
        font_size=sp(22),
        background_color=(1, 1, 1, 1),
        size_hint=(1, None),
        height=dp(280),
        halign="left"
    )
    app.product_name_input.bind(
        width=lambda instance, value: setattr(instance, 'text_size', (value, None))
    )
    layout.add_widget(app.product_name_input)

    # 🟩 Подпись "Сканируйте"
    app.label = Label(
        text="[b]Сканируйте штрихкод[/b]",
        markup=True,
        font_size=sp(18),
        halign="center",
        valign="middle",
        size_hint=(1, None),
        height=dp(40)
    )
    app.label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
    layout.add_widget(app.label)

    # 🟩 Штрихкод
    app.barcode_input = TextInput(
        hint_text="Штрихкод",
        multiline=False,
        size_hint=(1, None),
        height=dp(45),
        font_size=sp(18),
        background_color=(1, 1, 1, 1)
    )
    app.barcode_input.bind(on_text_validate=lambda instance: app.process_barcode())
    layout.add_widget(app.barcode_input)

    # 🟩 Количество
    app.qty_input = TextInput(
        hint_text="Количество",
        multiline=False,
        input_filter="int",
        size_hint=(1, None),
        height=dp(45),
        font_size=sp(18),
        background_color=(1, 1, 1, 1)
    )
    layout.add_widget(app.qty_input)

    # 🟩 Имя сотрудника
    app.employee_input = TextInput(
        hint_text="Имя Обязательно",
        multiline=False,
        size_hint=(1, None),
        height=dp(45),
        font_size=sp(18),
        background_color=(1, 1, 1, 1)
    )
    layout.add_widget(app.employee_input)

    # 🟩 Режимы (классические кнопки)
    mode_layout = BoxLayout(size_hint=(1, None), height=dp(45), spacing=dp(10))
    app.auto_btn = ToggleButton(text="Быстро", group="mode", state="down", font_size=sp(18))
    app.manual_btn = ToggleButton(text="Ручной", group="mode", font_size=sp(18))
    app.auto_btn.bind(on_press=lambda x: app.set_mode("auto"))
    app.manual_btn.bind(on_press=lambda x: app.set_mode("manual"))
    mode_layout.add_widget(app.auto_btn)
    mode_layout.add_widget(app.manual_btn)
    layout.add_widget(mode_layout)

    # 🟩 Кнопки "Добавить в список" и "Сохранить в Excel"
    actions_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

    app.add_button = Button(
        text="+в список",
        background_normal="",
        background_color=(0.0, 0.3647, 0.447, 1),
        color=(1, 1, 1, 1),
        font_size=sp(22)
    )
    app.add_button.bind(on_press=lambda instance: app.add_to_temp_list())
    actions_layout.add_widget(app.add_button)

    app.save_button = Button(
        text="в Excel",
        background_normal="",
        background_color=(0, 0.63, 0, 1),
        color=(1, 1, 1, 1),
        font_size=sp(20)
    )
    app.save_button.bind(on_press=lambda instance: save_csv(app, instance))
    actions_layout.add_widget(app.save_button)

    layout.add_widget(actions_layout)

    # 🟩 Загрузка баз из встроенного файла
    try:
        app.sadopt = get_sadopt_items()
        app.region = get_region_items()
        print("Встроенные базы загружены успешно")
    except Exception as e:
        print("Ошибка загрузки встроенных данных:", e)

    return layout
