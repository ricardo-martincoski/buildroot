import core.basetest
import subprocess
import os

def dumpe2fs_run(builddir, image):
    r = subprocess.check_output(["host/usr/sbin/dumpe2fs",
                                 os.path.join("images", image)],
                                stderr = open(os.devnull, "w"),
                                cwd = builddir,
                                env = { "LANG" : "C" })
    return r.strip().splitlines()

def dumpe2fs_getprop(out, prop):
    for l in out:
        l = l.split(": ")
        if l[0] == prop:
            return l[1].strip()

VOLNAME_PROP = "Filesystem volume name"
REVISION_PROP = "Filesystem revision #"
FEATURES_PROP = "Filesystem features"
BLOCKCNT_PROP = "Block count"
INODECNT_PROP = "Inode count"
RESBLKCNT_PROP = "Reserved block count"

class TestExt2(core.basetest.BRTest):
    config = core.basetest.basic_toolchain_config + """
BR2_TARGET_ROOTFS_EXT2=y
BR2_TARGET_ROOTFS_EXT2_2r0=y
BR2_TARGET_ROOTFS_EXT2_LABEL="foobaz"
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        out = dumpe2fs_run(self.builddir, "rootfs.ext2")
        self.assertEqual(dumpe2fs_getprop(out, VOLNAME_PROP),
                         "foobaz")
        self.assertEqual(dumpe2fs_getprop(out, REVISION_PROP),
                         "0 (original)")
        img = os.path.join(self.builddir, "images", "rootfs.ext2")
        self.s.boot(arch="armv7", kernel="builtin",
                    options=["-drive", "file=%s,if=sd" % img],
                    append=["root=/dev/mmcblk0", "rootfstype=ext2"])
        self.s.login()
        (r, s) = self.s.run("mount | grep '/dev/root on / type ext2'")
        self.assertEqual(s, 0)

class TestExt2r1(core.basetest.BRTest):
    config = core.basetest.basic_toolchain_config + """
BR2_TARGET_ROOTFS_EXT2=y
BR2_TARGET_ROOTFS_EXT2_2r1=y
BR2_TARGET_ROOTFS_EXT2_LABEL="foobar"
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        out = dumpe2fs_run(self.builddir, "rootfs.ext2")
        self.assertEqual(dumpe2fs_getprop(out, VOLNAME_PROP),
                         "foobar")
        self.assertEqual(dumpe2fs_getprop(out, REVISION_PROP),
                         "1 (dynamic)")
        self.assertNotIn("has_journal",
                         dumpe2fs_getprop(out, FEATURES_PROP))
        img = os.path.join(self.builddir, "images", "rootfs.ext2")
        self.s.boot(arch="armv7", kernel="builtin",
                    options=["-drive", "file=%s,if=sd" % img],
                    append=["root=/dev/mmcblk0", "rootfstype=ext2"])
        self.s.login()
        (r, s) = self.s.run("mount | grep '/dev/root on / type ext2'")
        self.assertEqual(s, 0)

class TestExt3(core.basetest.BRTest):
    config = core.basetest.basic_toolchain_config + """
BR2_TARGET_ROOTFS_EXT2=y
BR2_TARGET_ROOTFS_EXT2_3=y
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        out = dumpe2fs_run(self.builddir, "rootfs.ext3")
        self.assertEqual(dumpe2fs_getprop(out, REVISION_PROP),
                         "1 (dynamic)")
        self.assertIn("has_journal",
                      dumpe2fs_getprop(out, FEATURES_PROP))
        img = os.path.join(self.builddir, "images", "rootfs.ext3")
        self.s.boot(arch="armv7", kernel="builtin",
                    options=["-drive", "file=%s,if=sd" % img],
                    append=["root=/dev/mmcblk0", "rootfstype=ext3"])
        self.s.login()
        (r, s) = self.s.run("mount | grep '/dev/root on / type ext3'")
        self.assertEqual(s, 0)

class TestExt4(core.basetest.BRTest):
    config = core.basetest.basic_toolchain_config + """
BR2_TARGET_ROOTFS_EXT2=y
BR2_TARGET_ROOTFS_EXT2_4=y
BR2_TARGET_ROOTFS_EXT2_BLOCKS=16384
BR2_TARGET_ROOTFS_EXT2_INODES=3000
BR2_TARGET_ROOTFS_EXT2_RESBLKS=10
# BR2_TARGET_ROOTFS_TAR is not set
"""

    def test_run(self):
        out = dumpe2fs_run(self.builddir, "rootfs.ext4")
        self.assertEqual(dumpe2fs_getprop(out, REVISION_PROP),
                         "1 (dynamic)")
        self.assertEqual(dumpe2fs_getprop(out, BLOCKCNT_PROP),
                         "16384")
        # Yes there are 8 more inodes than requested
        self.assertEqual(dumpe2fs_getprop(out, INODECNT_PROP),
                         "3008")
        self.assertEqual(dumpe2fs_getprop(out, RESBLKCNT_PROP),
                         "1638")
        self.assertIn("has_journal",
                      dumpe2fs_getprop(out, FEATURES_PROP))
        self.assertIn("extent",
                      dumpe2fs_getprop(out, FEATURES_PROP))
        img = os.path.join(self.builddir, "images", "rootfs.ext4")
        self.s.boot(arch="armv7", kernel="builtin",
                    options=["-drive", "file=%s,if=sd" % img],
                    append=["root=/dev/mmcblk0", "rootfstype=ext4"])
        self.s.login()
        (r, s) = self.s.run("mount | grep '/dev/root on / type ext4'")
        self.assertEqual(s, 0)
