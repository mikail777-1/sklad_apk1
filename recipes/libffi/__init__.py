from pythonforandroid.recipe import Recipe
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
        configure_path = os.path.join(build_dir, "configure")

        if not os.path.exists(configure_path):
            print("⚙️ Running autogen.sh to generate configure")
            self.ctx.run("./autogen.sh", cwd=build_dir, env=env)

        configure = f"./configure --host={host} --prefix={build_dir}/install"
        self.ctx.run(configure, cwd=build_dir, env=env)
        self.ctx.run("make -j4", cwd=build_dir, env=env)
        self.ctx.run("make install", cwd=build_dir, env=env)

recipe = LibffiRecipe()
