import urllib
import tempfile
import os

baseurl = "http://free-electrons.com/~thomas/pub/buildroot-runtime-tests/"

def download(dldir, filename):
    finalpath = os.path.join(dldir, filename)
    if os.path.exists(finalpath):
        return finalpath
    if not os.path.exists(dldir):
        os.mkdir(dldir)
    tmpfile = tempfile.mktemp(dir=dldir)
    print "Downloading to %s" % tmpfile
    urllib.urlretrieve(os.path.join(baseurl, filename), tmpfile)
    print "Renaming from %s to %s" % (tmpfile, finalpath)
    os.rename(tmpfile, finalpath)
    return finalpath
