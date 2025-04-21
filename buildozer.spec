[app]

title = Склад Таврово-2, Белгород
package.name = sklad_tavrovo2
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,ttf,txt
version = 1.0
requirements = python3,kivy,sqlite3,pyjnius,openpyxl
orientation = portrait
fullscreen = 1

# Включаем AndroidX (для новых API Android)
android.enable_androidx = 1

# Разрешения (чтение/запись файлов)
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Минимальная и целевая версия Android
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.ndk_api = 24

# Архитектура
android.archs = armeabi-v7a

p4a.local_recipes = ./recipes

# Без дополнительных аргументов
android.extra_args =

# Локальные рецепты (sqlite3, если используешь)
android.local_recipes = ./recipes

# Лаунчер и тема
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.NoTitleBar

# (Опционально) Иконка приложения
# icon.filename = %(source.dir)s/icon.png

# (Опционально) Заставка
# presplash.filename = %(source.dir)s/presplash.png

# Копировать .so библиотеки
android.copy_libs = 1

# Поддержка ZIP
zip_safe = false
