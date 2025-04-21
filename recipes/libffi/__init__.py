from pythonforandroid.recipe import Recipe
import os
import subprocess


class LibffiRecipe(Recipe):
    version = '3.4.2'
    url = 'https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz'
    name = 'libffi'

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        env = self.get_build_env(arch)

        configure = ['./configure', '--host=arm-linux-androideabi', '--prefix=' + self.get_install_dir(arch.arch)]

        # Создаём configure, если его нет
        if not os.path.exists(os.path.join(build_dir, 'configure')):
            subprocess.run(['./autogen.sh'], cwd=build_dir, env=env, check=True)

        subprocess.run(configure, cwd=build_dir, env=env, check=True)
        subprocess.run(['make', '-j4'], cwd=build_dir, env=env, check=True)
        subprocess.run(['make', 'install'], cwd=build_dir, env=env, check=True)


recipe = LibffiRecipe()
