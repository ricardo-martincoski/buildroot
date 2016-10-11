# See support/scripts/check-package.txt before editing this file.
# Kconfig generates errors if someone introduces a typo like "boool" instead of
# "bool", so below check functions don't need to check for things already
# checked by running "make menuconfig".

# Notice: ignore 'imported but unused' from pyflakes for check functions.
from checkpackagelib import check_consecutive_empty_lines
from checkpackagelib import check_empty_last_line
from checkpackagelib import check_newline_at_eof
from checkpackagelib import check_trailing_space
