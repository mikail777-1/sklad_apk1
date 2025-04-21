from pythonforandroid.recipe import Recipe
import os
import subprocess


class LibffiRecipe(Recipe):
    version = '3.4.2'
    url = 'https://github.com/libffi/libffi/releases/download/v{version}/libffi-{version}.tar.gz'
    name = 'libffi'

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        install_dir = os.path.join(self.ctx.get_python_install_dir(arch), 'libffi')

        env = os.environ.copy()
        env.update(arch.get_env())

        configure = ['./configure',
                     '--host=arm-linux-androideabi',
                     f'--prefix={install_dir}']

        if not os.path.exists(os.path.join(build_dir, 'configure')) and os.path.exists(os.path.join(build_dir, 'autogen.sh')):
            subprocess.run(['./autogen.sh'], cwd=build_dir, env=env, check=True)

        subprocess.run(configure, cwd=build_dir, env=env, check=True)
        subprocess.run(['make', '-j4'], cwd=build_dir, env=env, check=True)
        subprocess.run(['make', 'install'], cwd=build_dir, env=env, check=True)


recipe = LibffiRecipe()
