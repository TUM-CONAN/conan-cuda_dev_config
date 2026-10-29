import os

from conan import ConanFile


class TestPackageConan(ConanFile):
    settings = "os", "arch"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def test(self):
        dep = self.dependencies[self.tested_reference_str.split("#")[0]]
        version = dep.conf_info.get("user.cuda_dev_config:cuda_version")
        root = dep.conf_info.get("user.cuda_dev_config:cuda_root")
        nvcc = os.path.join(root, "bin", "nvcc")
        if str(version) != str(dep.options.cuda_version) or not os.path.exists(nvcc):
            raise Exception(f"cuda_dev_config test_package: FAIL ({version} at {root})")
        self.output.info(f"cuda_dev_config test_package: PASS (CUDA {version} at {root})")
