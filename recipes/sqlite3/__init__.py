from pythonforandroid.recipe import Recipe


class Sqlite3Recipe(Recipe):
    version = '3.35.5'
    url = 'https://www.sqlite.org/2021/sqlite-amalgamation-3350500.zip'
    depends = []
    built_libraries = ['libsqlite3.a']

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        # ничего не нужно делать перед сборкой

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        self.apply_patches(arch)
        self.build_static_lib(arch, build_dir)


recipe = Sqlite3Recipe()
