import subprocess
import os
import core.basetest

class TestRootfsOverlay(core.basetest.BRTest):
    config = core.basetest.basic_toolchain_config + core.basetest.minimal_config + """
BR2_ROOTFS_OVERLAY="%s %s"
""" % (core.basetest.filePath("tests/core/rootfs-overlay1"),
       core.basetest.filePath("tests/core/rootfs-overlay2"))

    def test_run(self):
        ret = subprocess.call(["cmp",
                               core.basetest.filePath("tests/core/rootfs-overlay1/test-file1"),
                               os.path.join(self.builddir, "target", "test-file1")])
        self.assertEqual(ret, 0)
        ret = subprocess.call(["cmp",
                               core.basetest.filePath("tests/core/rootfs-overlay2/etc/test-file2"),
                               os.path.join(self.builddir, "target", "etc", "test-file2")])
        self.assertEqual(ret, 0)
