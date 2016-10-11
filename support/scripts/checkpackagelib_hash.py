# See support/scripts/check-package.txt before editing this file.
# The validity of the hashes itself is checked when building, so below check
# functions don't need to check for things already checked by running
# "make package-dirclean package-source".

import re

# Notice: ignore 'imported but unused' from pyflakes for check functions.
from checkpackagelib import check_consecutive_empty_lines
from checkpackagelib import check_empty_last_line
from checkpackagelib import check_newline_at_eof
from checkpackagelib import check_trailing_space


def _empty_line_or_comment(text):
    return text.strip() == "" or text.startswith("#")


FILENAME_WITH_SLASH = re.compile("/")


def check_hash_filename(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start or end or _empty_line_or_comment(text):
        return

    fields = text.split()
    if len(fields) < 3:
        return

    filename = fields[2]
    if FILENAME_WITH_SLASH.search(filename):
        return ["{}:{}: use filename without directory component"
                " ({}#adding-packages-hash)"
                .format(fname, lineno, args.manual_url),
                text]


def check_hash_number_of_fields(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start or end or _empty_line_or_comment(text):
        return

    fields = text.split()
    if len(fields) != 3:
        return ["{}:{}: expected three fields ({}#adding-packages-hash)"
                .format(fname, lineno, args.manual_url),
                text]


len_of_hash = {"md5": 32, "sha1": 40, "sha224": 56, "sha256": 64, "sha384": 96,
               "sha512": 128}


def check_hash_type(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start or end or _empty_line_or_comment(text):
        return

    fields = text.split()
    if len(fields) < 2:
        return

    hash_type, hexa = fields[:2]
    if hash_type == "none":
        return
    if hash_type not in len_of_hash.keys():
        return ["{}:{}: unexpected type of hash ({}#adding-packages-hash)"
                .format(fname, lineno, args.manual_url),
                text]
    if not re.match("^[0-9A-Fa-f]{%s}$" % len_of_hash[hash_type], hexa):
        return ["{}:{}: hash size does not match type "
                "({}#adding-packages-hash)"
                .format(fname, lineno, args.manual_url),
                text,
                "expected {} hex digits".format(len_of_hash[hash_type])]
