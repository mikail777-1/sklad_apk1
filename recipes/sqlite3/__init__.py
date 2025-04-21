from pythonforandroid.recipe import CythonRecipe

class Sqlite3Recipe(CythonRecipe):
    version = '3.35.5'
    url = 'https://www.sqlite.org/2021/sqlite-amalgamation-3350500.zip'
    name = 'sqlite3'

recipe = Sqlite3Recipe()
