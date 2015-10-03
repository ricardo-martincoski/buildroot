import unittest
import os
import subprocess
import datetime

from builder import Builder
from system import System

basic_toolchain_config = """
BR2_arm=y
BR2_TOOLCHAIN_EXTERNAL=y
BR2_TOOLCHAIN_EXTERNAL_CUSTOM=y
BR2_TOOLCHAIN_EXTERNAL_DOWNLOAD=y
BR2_TOOLCHAIN_EXTERNAL_URL="http://autobuild.buildroot.org/toolchains/tarballs/br-arm-full-2015.05-1190-g4a48479.tar.bz2"
BR2_TOOLCHAIN_EXTERNAL_GCC_4_7=y
BR2_TOOLCHAIN_EXTERNAL_HEADERS_3_10=y
BR2_TOOLCHAIN_EXTERNAL_LOCALE=y
# BR2_TOOLCHAIN_EXTERNAL_HAS_THREADS_DEBUG is not set
BR2_TOOLCHAIN_EXTERNAL_INET_RPC=y
BR2_TOOLCHAIN_EXTERNAL_CXX=y
"""

minimal_config = """
BR2_INIT_NONE=y
BR2_SYSTEM_BIN_SH_NONE=y
# BR2_PACKAGE_BUSYBOX is not set
# BR2_TARGET_ROOTFS_TAR is not set
"""

def filePath(relpath):
    return os.path.join(os.getcwd(), "support/testing", relpath)

class BRTest(unittest.TestCase):
    outputdir = None
    downloaddir = None
    logtofile = True

    def showMsg(self, msg):
        print "[%s/%s/%s] %s" % (os.path.basename(self.__class__.outputdir),
                                 self.testname,
                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 msg)
    def setUp(self):
        self.testname = self.__class__.__name__
        self.builddir = os.path.join(self.__class__.outputdir, self.testname)
        skip_build = os.path.exists(self.builddir)
        self.runlog = self.builddir + "-run.log"
        self.s = None
        self.showMsg("Starting")
        self.b = Builder(self.__class__.config, self.builddir, self.logtofile)
        if not skip_build:
            self.showMsg("Building")
            self.b.build()
            self.showMsg("Building done")
        self.s = System(self.builddir, self.downloaddir, self.logtofile)

    def tearDown(self):
        self.showMsg("Cleaning up")
        if self.s:
            self.s.stop()
        if self.b and not os.getenv("KEEP_BUILD"):
            self.b.delete()
