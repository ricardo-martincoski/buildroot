# See support/scripts/check-package.txt before editing this file.
# Kconfig generates errors if someone introduces a typo like "boool" instead of
# "bool", so below check functions don't need to check for things already
# checked by running "make menuconfig".

import re

# Notice: ignore 'imported but unused' from pyflakes for check functions.
from checkpackagelib import check_consecutive_empty_lines
from checkpackagelib import check_empty_last_line
from checkpackagelib import check_newline_at_eof
from checkpackagelib import check_trailing_space


def _empty_or_comment(text):
    line = text.strip()
    # ignore empty lines and comment lines indented or not
    return line == "" or line.startswith("#")


def _part_of_help_text(text):
    return text.startswith("\t  ")


# used in more than one function
entries_that_should_not_be_indented = [
    "choice", "comment", "config", "endchoice", "endif", "endmenu", "if",
    "menu", "menuconfig", "source"]


attributes_order_convention = {
    "bool": 1, "prompt": 1, "string": 1, "default": 2, "depends": 3,
    "select": 4, "help": 5}


def check_attributes_order(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_attributes_order.state = 0
        return
    if end or _empty_or_comment(text) or _part_of_help_text(text):
        return

    attribute = text.split()[0]

    if attribute in entries_that_should_not_be_indented:
        check_attributes_order.state = 0
        return
    if attribute not in attributes_order_convention.keys():
        return
    new_state = attributes_order_convention[attribute]
    wrong_order = check_attributes_order.state > new_state

    # save to process next line
    check_attributes_order.state = new_state

    if wrong_order:
        return ["{}:{}: attributes order: type, default, depends on,"
                " select, help ({}#_config_files)"
                .format(fname, lineno, args.manual_url),
                text]


HELP_TEXT_FORMAT = re.compile("^\t  .{,62}$")
URL_ONLY = re.compile("^(http|https|git)://\S*$")


def check_help_text(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_help_text.help_text = False
        return
    if end or _empty_or_comment(text):
        return

    entry = text.split()[0]

    if entry in entries_that_should_not_be_indented:
        check_help_text.help_text = False
        return
    if text.strip() == "help":
        check_help_text.help_text = True
        return

    if not check_help_text.help_text:
        return

    if HELP_TEXT_FORMAT.match(text.rstrip()):
        return
    if URL_ONLY.match(text.strip()):
        return
    return ["{}:{}: help text: <tab><2 spaces><62 chars>"
            " ({}#writing-rules-config-in)"
            .format(fname, lineno, args.manual_url),
            text,
            "\t  " + "123456789 " * 6 + "12"]


ENDS_WITH_BACKSLASH = re.compile(r"^[^#].*\\$")
entries_that_should_be_indented = [
    "bool", "default", "depends", "help", "prompt", "select", "string"]


def check_indent(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start or end or _empty_or_comment(text) or _part_of_help_text(text):
        check_indent.backslash = False
        return

    entry = text.split()[0]

    last_line_ends_in_backslash = check_indent.backslash

    # calculate for next line
    if ENDS_WITH_BACKSLASH.search(text):
        check_indent.backslash = True
    else:
        check_indent.backslash = False

    if last_line_ends_in_backslash:
        if text.startswith("\t"):
            return
        else:
            return ["{}:{}: continuation line should be indented using tabs"
                    .format(fname, lineno),
                    text]

    if entry in entries_that_should_be_indented:
        if not text.startswith("\t{}".format(entry)):
            return ["{}:{}: should be indented with one tab ({}#_config_files)"
                    .format(fname, lineno, args.manual_url),
                    text]
    elif entry in entries_that_should_not_be_indented:
        if not text.startswith(entry):
            return ["{}:{}: should not be indented".format(fname, lineno),
                    text]
