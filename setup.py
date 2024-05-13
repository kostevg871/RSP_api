from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.dist import Distribution
import glob
import shutil


class CustomInstallCommand(install):
    def run(self):
        # run the original install command
        install.run(self)

        # copy the .pyd and .dll files to site-packages
        module_dir = self.install_lib
        shutil.copy('RSP_api/libs/module_.pyd', module_dir)
        for dll in glob.glob("RSP_api/libs/*.so"):
            shutil.copy(dll, module_dir)


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(self):
        return True


setup(
    name='module_repack',
    version='1.0',
    description="A packaged version of the module",
    packages=find_packages(where="RSP_api"),
    package_dir={"": "RSP_api"},
    include_package_data=True,
    cmdclass={'install': CustomInstallCommand},
    distclass=BinaryDistribution
)