#!/usr/bin/env cuda
# -*- coding: utf-8 -*-

from conans import ConanFile
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import os
import re


# pylint: disable=W0201
class CUDADevConfigConan(ConanFile):
    name = "cuda_dev_config"
    version = "10.0"
    license = "Proprietary Dependency"
    export = ["LICENSE.md"]
    description = "Configuration of CUDA SDK for use as a development dependency."
    url = "https://github.com/ulricheck/conan-cuda_dev_config"
    author = "Ulrich Eck <ulrich.eck@tum.de>"
    options = { 
        "cuda_version": ["10.0", "9.0"],
        "cuda_root": "ANY",
        }
    default_options = "cuda_version=10.0", "cuda_root=/usr/local/cuda"
    settings = "os", "arch"
    build_policy = "missing"

    def package_id(self):
        self.info.header_only()
        self.info.options.cuda_version = self.cuda_version

    def package_info(self):
        if self.have_cuda_dev:
            self.cpp_info.bindirs = [cuda_bindir,]
            self.user_info.cuda_version = self.cuda_version
            self.user_info.cuda_root = self.settings.cuda_root
            self.env_info.path.append(os.path.dirname(self.cuda_bindir))

    @property
    def have_cuda_dev(self):
        if not self.cuda_version:
            return False
        if not os.path.exists(os.path.join(self.get_cuda_path("include"), 'cuda.h')):
            return False
        return True

    @property
    def cuda_version(self):
        if not hasattr(self, '_cuda_version'):
            cmd = "--version"
            result = self.run_nvcc_command(cmd)
            match = re.match(r".*, (\w+) (10.0).*", result.splitlines()[-1])
            if match and match.group(0) == "release":
                self._cuda_version = match.group(1)
                self.output.info("Found CUDA SDK: %s" % self._cuda_version)
            else:
                self.output.warning("Invalid response from calling nvcc --version: %r" % result)
                self._cuda_version = None
        return self._cuda_version

    @property
    def cuda_bindir(self):
        return self.get_cuda_path("bin")

    def get_cuda_path(self, dir_name):
        return os.path.join(self.settings.cuda_root, dir_name)

    def run_nvcc_command(self, cmd):
        nvcc_executable = os.path.join(self.cuda_bindir, "nvcc")
        output = StringIO()
        self.output.info('running command: "{0}" {1}'.format(nvcc_executable, cmd))
        self.run('"{0}" {1}'.format(nvcc_executable, cmd), output=output)
        result = output.getvalue().strip()
        return result if result and result != "" else None
