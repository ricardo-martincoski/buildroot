# See support/scripts/check-package.txt before editing this file.
# There are already dependency checks during the build, so below check
# functions don't need to check for things already checked by exploring the
# menu options using "make menuconfig" and by running "make" with appropriate
# packages enabled.

import re

# Notice: ignore 'imported but unused' from pyflakes for check functions.
from checkpackagelib import check_consecutive_empty_lines
from checkpackagelib import check_empty_last_line
from checkpackagelib import check_newline_at_eof
from checkpackagelib import check_trailing_space

# used by more than one function
ENDS_WITH_BACKSLASH = re.compile(r"^[^#].*\\$")

COMMENT = re.compile("^\s*#")
CONDITIONAL = re.compile("^\s*(ifeq|ifneq|endif)\s")
END_DEFINE = re.compile("^\s*endef\s")
MAKEFILE_TARGET = re.compile("^[^# \t]+:\s")
START_DEFINE = re.compile("^\s*define\s")


def check_indent(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_indent.define = False
        check_indent.backslash = False
        check_indent.makefile_target = False
        return
    if end:
        return

    if START_DEFINE.search(text):
        check_indent.define = True
        return
    if END_DEFINE.search(text):
        check_indent.define = False
        return

    expect_tabs = False
    if (check_indent.define or check_indent.backslash or
            check_indent.makefile_target):
        expect_tabs = True
    if CONDITIONAL.search(text):
        expect_tabs = False

    # calculate for next line
    if ENDS_WITH_BACKSLASH.search(text):
        check_indent.backslash = True
    else:
        check_indent.backslash = False

    if MAKEFILE_TARGET.search(text):
        check_indent.makefile_target = True
        return
    if text.strip() == "":
        check_indent.makefile_target = False
        return

    # comment can be indented or not inside define ... endef, so ignore it
    if check_indent.define and COMMENT.search(text):
        return

    if expect_tabs:
        if not text.startswith("\t"):
            return ["{}:{}: expected indent with tabs"
                    .format(fname, lineno),
                    text]
    else:
        if text.startswith("\t"):
            return ["{}:{}: unexpected indent with tabs"
                    .format(fname, lineno),
                    text]


def check_package_header(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_package_header.skip = False
        return
    if end or check_package_header.skip or lineno > 6:
        return

    if lineno in [1, 5]:
        if lineno == 1 and text.startswith("include "):
            check_package_header.skip = True
            return
        if text.rstrip() != "#" * 80:
            return ["{}:{}: should be 80 hashes ({}#writing-rules-mk)"
                    .format(fname, lineno, args.manual_url),
                    text,
                    "#" * 80]
    elif lineno in [2, 4]:
        if text.rstrip() != "#":
            return ["{}:{}: should be 1 hash ({}#writing-rules-mk)"
                    .format(fname, lineno, args.manual_url),
                    text]
    elif lineno == 6:
        if text.rstrip() != "":
            return ["{}:{}: should be a blank line ({}#writing-rules-mk)"
                    .format(fname, lineno, args.manual_url),
                    text]


TAB_OR_MULTIPLE_SPACES_BEFORE_BACKSLASH = re.compile(r"^.*(  |\t)\\$")


def check_space_before_backslash(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start or end:
        return

    if TAB_OR_MULTIPLE_SPACES_BEFORE_BACKSLASH.match(text.rstrip()):
        return ["{}:{}: use only one space before backslash"
                .format(fname, lineno),
                text]


def check_trailing_backslash(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_trailing_backslash.backslash = False
        return
    if end:
        return

    last_line_ends_in_backslash = check_trailing_backslash.backslash

    # calculate for next line
    if ENDS_WITH_BACKSLASH.search(text):
        check_trailing_backslash.backslash = True
        check_trailing_backslash.lastline = text
        return
    check_trailing_backslash.backslash = False

    if last_line_ends_in_backslash and text.strip() == "":
        return ["{}:{}: remove trailing backslash"
                .format(fname, lineno - 1),
                check_trailing_backslash.lastline]


ALLOWED = re.compile("|".join([
    "ACLOCAL_DIR",
    "ACLOCAL_HOST_DIR",
    "BR_CCACHE_INITIAL_SETUP",
    "BR_NO_CHECK_HASH_FOR",
    "LINUX_POST_PATCH_HOOKS",
    "LINUX_TOOLS",
    "LUA_RUN",
    "MKFS_JFFS2",
    "MKIMAGE_ARCH",
    "PKG_CONFIG_HOST_BINARY",
    "TARGET_FINALIZE_HOOKS",
    "XTENSA_CORE_NAME"]))
PACKAGE_NAME = re.compile("/([^/]+)\.mk")
VARIABLE = re.compile("^([A-Z0-9_]+_[A-Z0-9_]+)\s*(\+|)=")


def check_typo_in_package_variable(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        package = PACKAGE_NAME.search(fname).group(1).replace("-", "_").upper()
        # linux tools do not use LINUX_TOOL_ prefix for variables
        package = package.replace("LINUX_TOOL_", "")
        check_typo_in_package_variable.package = package
        check_typo_in_package_variable.REGEX = re.compile(
            "^(HOST_)?({}_[A-Z0-9_]+)".format(package))
        return
    if end:
        return

    m = VARIABLE.search(text)
    if m is None:
        return

    variable = m.group(1)
    if ALLOWED.match(variable):
        return
    if check_typo_in_package_variable.REGEX.search(text) is None:
        return ["{}:{}: possible typo: {} -> *{}*"
                .format(fname, lineno, variable,
                        check_typo_in_package_variable.package),
                text]


DEFAULT_AUTOTOOLS_FLAG = re.compile("^.*{}".format("|".join([
    "_AUTORECONF\s*=\s*NO",
    "_LIBTOOL_PATCH\s*=\s*YES"])))
DEFAULT_GENERIC_FLAG = re.compile("^.*{}".format("|".join([
    "_INSTALL_IMAGES\s*=\s*NO",
    "_INSTALL_REDISTRIBUTE\s*=\s*YES",
    "_INSTALL_STAGING\s*=\s*NO",
    "_INSTALL_TARGET\s*=\s*YES"])))
END_CONDITIONAL = re.compile("^\s*(endif)")
START_CONDITIONAL = re.compile("^\s*(ifeq|ifneq)")


def check_useless_flag(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_useless_flag.conditional = 0
        return
    if end:
        return

    if START_CONDITIONAL.search(text):
        check_useless_flag.conditional += 1
        return
    if END_CONDITIONAL.search(text):
        check_useless_flag.conditional -= 1
        return

    # allow non-default conditionally overridden by default
    if check_useless_flag.conditional > 0:
        return

    if DEFAULT_GENERIC_FLAG.search(text):
        return ["{}:{}: useless default value "
                "({}#_infrastructure_for_packages_with_specific_build_systems)"
                .format(fname, lineno, args.manual_url),
                text]

    if DEFAULT_AUTOTOOLS_FLAG.search(text):
        return ["{}:{}: useless default value "
                "({}#_infrastructure_for_autotools_based_packages)"
                .format(fname, lineno, args.manual_url),
                text]
