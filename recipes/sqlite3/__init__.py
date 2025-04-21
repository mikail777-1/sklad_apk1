from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory, ensure_dir
import os
import shlex
import subprocess


class Sqlite3Recipe(Recipe):
    version = '3380500'
    url = 'https://www.sqlite.org/2022/sqlite-autoconf-{version}.tar.gz'
    name = 'sqlite3'
    built_libraries = {'libsqlite3.a': 'lib/libsqlite3.a'}
    def get_lib_dir(self, arch):
        return os.path.join(self.get_build_dir(arch), 'lib')

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        install_dir = os.path.join(self.ctx.get_python_install_dir(arch.arch), 'sqlite3')
        ensure_dir(install_dir)

        with current_directory(build_dir):
            configure = shlex.split(f'./configure --host={arch.command_prefix} --prefix={install_dir} --disable-shared --enable-static')
            env = arch.get_env()
            subprocess.check_call(configure, env=env)
            subprocess.check_call(['make', '-j4'], env=env)
            subprocess.check_call(['make', 'install'], env=env)

    def should_build(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        lib_path = os.path.join(self.ctx.get_python_install_dir(arch.arch), 'sqlite3', 'lib', 'libsqlite3.a')
        return not os.path.exists(lib_path)


recipe = Sqlite3Recipe()
