# See support/scripts/check-package.txt before editing this file.
# There are already dependency checks during the build, so below check
# functions don't need to check for things already checked by exploring the
# menu options using "make menuconfig" and by running "make" with appropriate
# packages enabled.

# Notice: ignore 'imported but unused' from pyflakes for check functions.
from checkpackagelib import check_consecutive_empty_lines
from checkpackagelib import check_empty_last_line
from checkpackagelib import check_newline_at_eof
from checkpackagelib import check_trailing_space
