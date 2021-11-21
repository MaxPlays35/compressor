#
# Font decorations
#
BOLD = '\x1b[1m'
UNDERLINE = '\x1b[4m'

#
# Text color
#
GREEN = '\x1b[32m'
LIGHT_BLUE = '\x1b[36m'
LIGHT_YELLOW = '\x1b[93m'
LIGHT_RED = '\x1b[91m'
RED = "\x1b[31m"

#
# Mixes
#
STEP_DEC = BOLD + LIGHT_YELLOW
RESULT_DEC = UNDERLINE + GREEN
HEADER = STEP_DEC

#
# Color and font reset
#
RESET_COLOR = '\x1b[39m'
RESET_FONT = '\x1b[0m'
RESET = RESET_COLOR + RESET_FONT