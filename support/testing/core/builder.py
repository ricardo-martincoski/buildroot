import os
import shutil
import subprocess
import sys

class Builder:
    def __init__(self, config, builddir, logtofile):
        self.config = config
        self.builddir = builddir
        self.logtofile = logtofile

    def build(self):
        os.mkdir(self.builddir)
        if self.logtofile:
            log = open(self.builddir + "-build.log", "w+")
        else:
            log = sys.stdout
        f = open(os.path.join(self.builddir, ".config"), "w+")
        f.write(self.config)
        f.close()
        cmd = ["make", "-C", os.getcwd(), "O=%s" % self.builddir, "olddefconfig"]
        ret = subprocess.call(cmd, stdout=log, stderr=log)
        if ret != 0:
            raise SystemError("Cannot olddefconfig")
        cmd = ["make", "-C", self.builddir]
        ret = subprocess.call(cmd, stdout=log, stderr=log)
        if ret != 0:
            raise SystemError("Build failed")

    def delete(self):
        shutil.rmtree(self.builddir)
