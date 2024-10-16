#!/usr/bin/env cuda
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.errors import ConanException
from conan.tools.files import save
import os


def get_path(conanfile, filepath):
    "For Windows, Converts the given path into 8.3 (DOS) form equivalent to work with e.g. pkgconfig."
    if not (conanfile.settings.os == "Windows" or conanfile.settings.os == "WindowsStore"):
        return filepath

    import win32api, os
    if filepath[-1] == "/":
        filepath = filepath[:-1]
    tokens = os.path.normpath(filepath).split("\\")
    if len(tokens) == 1:
        return filepath
    ShortPath = tokens[0]
    for token in tokens[1:]:
        PartPath = "/".join([ShortPath, token])
        Found = win32api.FindFiles(PartPath)
        if Found == []:
            raise WindowsError('The system cannot find the path specified: "{0}"'.format(PartPath))
        else:
            if Found[0][9] == "":
                ShortToken = token
            else:
                ShortToken = Found[0][9]
            ShortPath = ShortPath + "/" + ShortToken
    return ShortPath

# pylint: disable=W0201
class CUDADevConfigConan(ConanFile):
    python_requires = "camp_common/0.5@camposs/stable"
    python_requires_extend = "camp_common.CampCudaBase"

    name = "cuda_dev_config"
    version = "2.2"
    package_type = "shared-library"

    license = "Proprietary Dependency"
    exports = ["LICENSE.md"]
    description = "Configuration of CUDA SDK for use as a development dependency."
    url = "https://github.com/TUM-CONAN/conan-cuda_dev_config"
    author = "Ulrich Eck <ulrich.eck@tum.de>"
    options = {
        "shared": [True, False],
        "cuda_version": ["12.6","12.5","12.4","12.3","12.2","12.1","12.0",
                         "11.8","11.7","11.6","11.5","11.4","11.2","11.1","11.0",
                         "10.2", "10.1", "10.0"],
        "cuda_root": ["ANY", ],
        "cuda_archs": ["ANY",],
        }
    default_options = {
        'shared': True,
        "cuda_version": "11.8",
        "cuda_root": "ANY",
        "cuda_archs": "75,86",
    }

    settings = "os", "arch"
    build_policy = "missing"

    def system_requirements(self):
        if not os.path.exists(self._cuda_include_dir):
            raise ConanException("CUDA runtime include directory: {} not found", self._cuda_include_dir)
        if not os.path.exists(self._cuda_lib_dir):
            raise ConanException("CUDA runtime library : {} not found", self._cuda_lib_dir)
        if not os.path.exists(self._cuda_bin_dir):
            raise ConanException("nvcc : {} not found", self._cuda_bin_dir)

    def package_id(self):
        self.info.clear()

    def package(self):
        save(self, os.path.join(self.package_folder, "include", "dummy.txt"), "placeholder")

    def package_info(self):
        if self.have_cuda_toolkit:
            self.cpp_info.includedirs = [get_path(self, self._cuda_include_dir), ]
            self.cpp_info.system_libs.append(self._cuda_runtime_ldname)

            # self.cpp_info.resdirs
            self.cpp_info.libdirs.append(get_path(self, self._cuda_lib_dir))
            self.cpp_info.bindirs.append(get_path(self, self._cuda_bin_dir))

            # buildenv_info here
            cuda_archs = ";".join(str(self.options.cuda_archs).split(","))

            self.buildenv_info.append_path("PATH", get_path(self, self._cuda_lib_dir))
            self.buildenv_info.append_path("PATH", get_path(self, self._cuda_bin_dir))
            self.buildenv_info.define_path("CUDA_SDK_ROOT_DIR", self._cuda_sdk_root)
            self.buildenv_info.define_path("CUDAARCHS", cuda_archs)

            self.conf_info.define("cuda_dev_config:cuda_version", self._cuda_version)
            self.conf_info.define("cuda_dev_config:cuda_root", get_path(self, self._cuda_sdk_root))
            self.conf_info.define("cuda_dev_config:cuda_archs", cuda_archs)

    @property
    def have_cuda_toolkit(self):
        if not os.path.exists(self._cuda_include_dir):
            return False
        if not os.path.exists(self._cuda_lib_dir):
            return False
        if not os.path.exists(self._cuda_bin_dir):
            return False
        return True
