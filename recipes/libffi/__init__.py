from pythonforandroid.recipe import Recipe
from pythonforandroid.util import sh  # 💡 добавляем это
import os

class LibffiRecipe(Recipe):
    version = "3.4.2"
    url = "https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz"
    name = "libffi"

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        env = self.get_recipe_env(arch)
        self.apply_patches(arch)
        print("⚙️ Building libffi...")

        host = arch.command_prefix.strip("-")
        configure = f"./configure --host={host} --prefix={build_dir}/install"
        sh(configure, cwd=build_dir, env=env)
        sh("make -j4", cwd=build_dir, env=env)
        sh("make install", cwd=build_dir, env=env)

recipe = LibffiRecipe()
