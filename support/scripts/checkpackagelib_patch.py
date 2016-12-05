# See support/scripts/check-package.txt before editing this file.
# The format of the patch files is tested during the build, so below check
# functions don't need to check for things already checked by running
# "make package-dirclean package-patch".

import re

# Notice: ignore 'imported but unused' from pyflakes for check functions.
from checkpackagelib import check_newline_at_eof


APPLY_ORDER = re.compile("/\d{1,4}-[^/]*$")


def check_apply_order(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start and not APPLY_ORDER.search(fname):
        return ["{}:0: use name <number>-<description>.patch "
                "({}#_providing_patches)".format(fname, args.manual_url)]


NUMBERED_PATCH = re.compile("Subject:\s*\[PATCH\s*\d+/\d+\]")


def check_numbered_subject(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start or end:
        return
    if NUMBERED_PATCH.search(text):
        return ["{}:{}: generate your patches with 'git format-patch -N'"
                .format(fname, lineno),
                text]


SOB_ENTRY = re.compile("^Signed-off-by: .*$")


def check_sob(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_sob.found = False
        return
    if check_sob.found:
        return
    if end:
        return ["{}:0: missing Signed-off-by in the header "
                "({}#_format_and_licensing_of_the_package_patches)"
                .format(fname, args.manual_url)]
    if SOB_ENTRY.search(text):
        check_sob.found = True
