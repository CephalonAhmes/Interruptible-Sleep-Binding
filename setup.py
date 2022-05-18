import setuptools
from setuptools.command.build_ext import build_ext
import struct
import os
import glob
import shutil
import pathlib

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

        build_dir = pathlib.Path(self.build_temp)

        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        # Now that the necessary directories are created, build

        self.announce("Configuring cmake project", level=3)

        # Change your cmake arguments below as necessary
        # Below is just an example set of arguments for building Blender as a Python module

        self.spawn(['cmake', '-S'+RootDirectory, '-B'+self.build_temp,
                    '-DWITH_PLAYER=OFF', '-DWITH_PYTHON_INSTALL=OFF',
                    '-DWITH_PYTHON_MODULE=ON',
                ])

        self.announce("Building binaries", level=3)

        self.spawn(["cmake", "--build", self.build_temp, "--target", CMAKE_Target_Name,
                    "--config", "Release"])

        # Build finished, now copy the files into the copy directory
        # The copy directory is the parent directory of the extension (.pyd)

        self.announce("Moving built python module", level=3)

        bin_dir = os.path.join(build_dir, 'Release')
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


setuptools.setup(name='InterruptibleSleepBinding',
                 version=os.environ.get('VERSIONNUMBER', "0.0.0"),
                 ext_modules=[CMakeExtension(
                     name="InterruptibleSleepBinding")],
                 description="A single-function module created in c++ to get around time.sleep()'s limitations when handling signals",
                 long_description=open("./README.md", 'r').read(),
                 long_description_content_type="text/markdown",
                 keywords="test, cmake, extension",
                 classifiers=["Intended Audience :: Developers",
                              "License :: OSI Approved :: "
                              "GNU Lesser General Public License v3 (LGPLv3)",
                              "Natural Language :: English",
                              "Programming Language :: C++",
                              "Programming Language :: Python",
                              "Programming Language :: Python :: Implementation :: CPython"],
                 license='GPL-3.0',
                 cmdclass={
                     'build_ext': BuildCMakeExt,
                     'clean': CleanCommand,
                 },
                 )
