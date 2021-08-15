#!/usr/bin/env cuda
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os

# pylint: disable=W0201
class CUDADevConfigConan(ConanFile):
    python_requires = "camp_common/[>=0.1]@camposs/stable"
    python_requires_extend = "camp_common.CampCudaBase"

    name = "cuda_dev_config"
    version = "2.0"
    license = "Proprietary Dependency"
    exports = ["LICENSE.md"]
    description = "Configuration of CUDA SDK for use as a development dependency."
    url = "https://github.com/ulricheck/conan-cuda_dev_config"
    author = "Ulrich Eck <ulrich.eck@tum.de>"
    options = { 
        "cuda_version": ["11.4","11.2","11.1","11.0","10.2", "10.1", "10.0", "9.1", "9.0"],
        "cuda_root": "ANY",
        }
    default_options = {
        "cuda_version": "11.1", 
        "cuda_root": "ANY",
    }

    settings = "os", "arch"
    build_policy = "missing"

    def validate(self):
        assert(self.have_cuda_dev)


    def package_info(self):
        if self.have_cuda_dev:
            self.cpp_info.bindirs = [self._cuda_bin_dir,]
            self.user_info.cuda_version = self._cuda_version
            self.user_info.cuda_root = self._cuda_sdk_root
            self.env_info.path.append(self._cuda_sdk_root)
            self.env_info.CUDA_SDK_ROOT_DIR = self._cuda_sdk_root

    @property
    def have_cuda_dev(self):
        if not self._cuda_version:
            return False
        if not os.path.exists(os.path.join(self._cuda_include_dir, 'cuda.h')):
            return False
        return True
