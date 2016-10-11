# See support/scripts/check-package.txt before editing this file.


def check_consecutive_empty_lines(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_consecutive_empty_lines.lastline = "non empty"
        return
    if end:
        return
    if text.strip() == "" == check_consecutive_empty_lines.lastline.strip():
        return ["{}:{}: consecutive empty lines".format(fname, lineno)]
    check_consecutive_empty_lines.lastline = text


def check_empty_last_line(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_empty_last_line.lastlineno = 0
        check_empty_last_line.lastline = "non empty"
        return
    if end:
        if check_empty_last_line.lastline.strip() == "":
            return ["{}:{}: empty line at end of file"
                    .format(fname, check_empty_last_line.lastlineno)]
        return
    check_empty_last_line.lastlineno = lineno
    check_empty_last_line.lastline = text


def check_newline_at_eof(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start:
        check_newline_at_eof.lastlineno = 0
        check_newline_at_eof.lastline = "\n"
        return
    if end:
        line = check_newline_at_eof.lastline
        if line == line.rstrip("\r\n"):
            return ["{}:{}: missing newline at end of file"
                    .format(fname, check_newline_at_eof.lastlineno),
                    line]
        return
    check_newline_at_eof.lastlineno = lineno
    check_newline_at_eof.lastline = text


def check_trailing_space(
        fname, args, lineno=0, text=None, start=False, end=False):
    if start or end:
        return
    line = text.rstrip("\r\n")
    if line != line.rstrip():
        return ["{}:{}: line contains trailing whitespace"
                .format(fname, lineno),
                text]
