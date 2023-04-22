#!/usr/bin/env cuda
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.errors import ConanException
import os

# pylint: disable=W0201
class CUDADevConfigConan(ConanFile):
    python_requires = "camp_common/0.5@camposs/stable"
    python_requires_extend = "camp_common.CampCudaBase"

    name = "cuda_dev_config"
    version = "2.1"
    license = "Proprietary Dependency"
    exports = ["LICENSE.md"]
    description = "Configuration of CUDA SDK for use as a development dependency."
    url = "https://github.com/TUM-CONAN/conan-cuda_dev_config"
    author = "Ulrich Eck <ulrich.eck@tum.de>"
    options = {
        "shared": [True, False],
        "cuda_version": ["12.1","12.0","11.8","11.7","11.6","11.5","11.4","11.2","11.1","11.0","10.2", "10.1", "10.0"],
        "cuda_root": ["ANY", ],
        }
    default_options = {
        'shared': True,
        "cuda_version": "11.7",
        "cuda_root": "ANY",
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

    def package_info(self):
        if self.have_cuda_toolkit:
            self.cpp_info.includedirs.append(self._cuda_include_dir)
            self.cpp_info.libs.append(self._cuda_runtime_ldname)

            # self.cpp_info.resdirs
            self.cpp_info.libdirs.append(self._cuda_lib_dir)
            self.cpp_info.bindirs.append(self._cuda_bin_dir)

            # buildenv_info here
            self.buildenv_info.append_path("PATH", self._cuda_lib_dir)
            self.buildenv_info.append_path("PATH", self._cuda_bin_dir)
            self.buildenv_info.define_path("CUDA_SDK_ROOT_DIR", self._cuda_sdk_root)

            self.conf_info.define("cuda_dev_config:cuda_version", self._cuda_version)
            self.conf_info.define("cuda_dev_config:cuda_root", self._cuda_sdk_root)

    @property
    def have_cuda_toolkit(self):
        if not os.path.exists(self._cuda_include_dir):
            return False
        if not os.path.exists(self._cuda_lib_dir):
            return False
        if not os.path.exists(self._cuda_bin_dir):
            return False
        return True
