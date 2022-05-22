import setuptools
from setuptools.command.build_ext import build_ext
import os, sys, io
import glob
import shutil
import pathlib, json

CMAKE_Target_Name = "PythonBinding"
RootDirectory = os.path.dirname(os.path.abspath(__file__))


class CMakeExtension(setuptools.Extension):
    """
    An extension to run the cmake build

    This simply overrides the base extension class so that setuptools
    doesn't try to build your sources for you
    """

    def __init__(self, name, sources=[]):

        super().__init__(name=name, sources=sources)


class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
        """

        for extension in self.extensions:

            if extension.name == 'InterruptibleSleepBinding':

                self.build_cmake(extension)

        super().run()

    def build_cmake(self, extension: setuptools.Extension):
        """
        The steps required to build the extension
        """

        self.announce("Preparing the build environment", level=3)
        self.build_dir = pathlib.Path("./build/")
        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(self.build_dir, exist_ok=True)
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)


        self.announce(f"Configuring cmake project to location {self.build_dir}", level=3)
        self.spawn(['cmake', '-S'+RootDirectory, '-B'+str(self.build_dir),
                    '-DWITH_PLAYER=OFF', '-DWITH_PYTHON_INSTALL=OFF',
                    '-DWITH_PYTHON_MODULE=ON', "-DPYTHON_EXECUTABLE:FILEPATH="+sys.executable
                ])

        self.announce(f"Building binaries to location {self.build_dir}", level=3)
        self.spawn(["cmake", "--build", str(self.build_dir), "--target", CMAKE_Target_Name,
                    "--config", "Release"])


        bin_dir = os.path.join(RootDirectory, './build/lib')
        self.announce(f"Moving built python module out of {bin_dir}", level=3)
        self.distribution.bin_dir = bin_dir

        pyd_path = [os.path.join(bin_dir, _pyd) for _pyd in
                    os.listdir(bin_dir) if
                    os.path.isfile(os.path.join(bin_dir, _pyd)) and
                    os.path.splitext(_pyd)[0].startswith(CMAKE_Target_Name) and
                    os.path.splitext(_pyd)[1] in [".pyd", ".so"]][0]

        shutil.move(pyd_path, extension_path)


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        files_to_delete = glob.glob('./*.egg-info/', recursive=False)
        for file_to_delete in files_to_delete:
            shutil.rmtree(file_to_delete)


def get_version_number():
    if os.path.isfile("package_version.json"):
        with io.open("package_version.json", mode='r', encoding='utf-8-sig') as file:
            data = json.load(file)

        return data['VERSIONNUMBER']

    return os.environ.get('VERSIONNUMBER', "0.0.0")


setuptools.setup(name='InterruptibleSleepBinding',
                 version=get_version_number(),
                 ext_modules=[CMakeExtension(
                     name="InterruptibleSleepBinding")],
                 description="A single-function module created in c++ to get around time.sleep()'s limitations when handling signals",
                 long_description=open("./README.md", 'r').read(),
                 long_description_content_type="text/markdown",
                 keywords="test, cmake, extension",
                 url="https://github.com/CephalonAhmes/Interruptible-Sleep-Binding",
                 classifiers=["Intended Audience :: Developers",
                              "License :: OSI Approved :: MIT License",
                              "Natural Language :: English",
                              "Programming Language :: C++",
                              "Programming Language :: Python",
                              "Programming Language :: Python :: Implementation :: CPython",
                              "Topic :: Software Development :: Libraries :: Python Modules"
                              ],
                 license_files = ('LICENSE',),
                 cmdclass={
                     'build_ext': BuildCMakeExt,
                     'clean': CleanCommand,
                 },
                 )
