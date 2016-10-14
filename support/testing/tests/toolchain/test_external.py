import core.basetest
import subprocess
import os

class TestExternalToolchain(core.basetest.BRTest):
    def get_file_arch(self, prefix, fpath):
        out = subprocess.check_output(["host/usr/bin/%s-readelf" % prefix,
                                       "-A", os.path.join("target", fpath)],
                                      cwd = self.builddir,
                                      env = {"LANG" : "C" })
        out = out.splitlines()
        for l in out:
            l = l.strip()
            if not l.startswith("Tag_CPU_arch:"):
                continue
            return l.split(":")[1].strip()
        return None

class TestExternalToolchainSourceryArmv4(TestExternalToolchain):
    config = """
BR2_arm=y
BR2_arm920t=y
BR2_TOOLCHAIN_EXTERNAL=y
BR2_TOOLCHAIN_EXTERNAL_CODESOURCERY_ARM=y
BR2_TARGET_ROOTFS_CPIO=y
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        arch = self.get_file_arch("arm-none-linux-gnueabi", "lib/libc.so.6")
        self.assertEqual(arch, "v4T")
        img = os.path.join(self.builddir, "images", "rootfs.cpio")
        self.s.boot(arch="armv5", kernel="builtin",
                    options=["-initrd", img])
        self.s.login("root")
