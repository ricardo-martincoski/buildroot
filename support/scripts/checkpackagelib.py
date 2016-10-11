# See support/scripts/check-package.txt before editing this file.


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
