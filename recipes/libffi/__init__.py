from pythonforandroid.recipe import CMakeRecipe

class LibffiRecipe(CMakeRecipe):
    version = '3.4.2'
    url = 'https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz'
    name = 'libffi'

recipe = LibffiRecipe()
