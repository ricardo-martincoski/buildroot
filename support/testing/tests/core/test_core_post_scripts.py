import core.basetest
import subprocess
import os

class TestPostScripts(core.basetest.BRTest):
    config = core.basetest.basic_toolchain_config + """
BR2_INIT_NONE=y
BR2_SYSTEM_BIN_SH_NONE=y
# BR2_PACKAGE_BUSYBOX is not set
BR2_ROOTFS_POST_BUILD_SCRIPT="%s"
BR2_ROOTFS_POST_IMAGE_SCRIPT="%s"
BR2_ROOTFS_POST_SCRIPT_ARGS="foobar baz"
""" % (core.basetest.filePath("tests/core/post-build.sh"),
       core.basetest.filePath("tests/core/post-image.sh"))

    def check_post_log_file(self,path):
        f = open(path, "r")
        lines = f.readlines()
        ## TODO

    def test_run(self):
        self.check_post_log_file(os.path.join(self.builddir, "build", "post-build.log"))
        self.check_post_log_file(os.path.join(self.builddir, "build", "post-image.log"))
