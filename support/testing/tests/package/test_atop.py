import os

import core.basetest

def get_package_version():
    for l in open(core.basetest.filePath("../../package/atop/atop.mk"), "r"):
        if l.startswith("ATOP_VERSION"):
            return l.split("=")[1].strip().replace(".", "\\.")

class TestAtop(core.basetest.BRTest):
    config = core.basetest.basic_toolchain_config + \
"""
BR2_PACKAGE_ATOP=y
BR2_TARGET_ROOTFS_CPIO=y
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        cpio_file = os.path.join(self.builddir, "images", "rootfs.cpio")
        self.s.boot(arch="armv5",
                           kernel="builtin",
                           options=["-initrd", cpio_file])
        self.s.login()

        cmd = "atop -V | grep '{}'".format(get_package_version())
        _, exit_code = self.s.run(cmd)
        self.assertEqual(exit_code, 0)

        cmd = "atop -a 1 2 | grep '% *atop *$'"
        _, exit_code = self.s.run(cmd)
        self.assertEqual(exit_code, 0)
