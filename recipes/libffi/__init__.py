from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory, sh
import os


class LibffiRecipe(Recipe):
    version = "3.3"
    url = "https://github.com/libffi/libffi/releases/download/v3.3/libffi-3.3.tar.gz"
    name = "libffi"

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch)
        install_dir = os.path.join(self.ctx.get_python_install_dir(arch), 'libffi')

        env = os.environ.copy()
        env['CC'] = self.get_recipe_env(arch)['CC']
        env['AR'] = self.get_recipe_env(arch)['AR']
        env['RANLIB'] = self.get_recipe_env(arch)['RANLIB']

        configure = ['./configure', f'--host={arch.command_prefix}', f'--prefix={install_dir}', '--disable-shared', '--enable-static']
        with current_directory(build_dir):
            sh(*configure, env=env)
            sh('make', env=env)
            sh('make', 'install', env=env)

    def get_include_dirs(self, arch):
        return [os.path.join(self.get_build_dir(arch), 'include')]
