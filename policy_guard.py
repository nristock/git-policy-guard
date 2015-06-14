import sys

from Logging import setup_logging
from hooks.pre_receive import execute as pre_receive
from hooks.post_receive import execute as post_receive
from hooks.update import execute as update

HOOK_TYPE = sys.argv[1]

if __name__ == '__main__':
    setup_logging()

    from settings import PLUGINS, DEBUG_PRE_RECEIVE, DEBUG_UPDATE, DEBUG_POST_RECEIVE

    ret_code = 0
    if HOOK_TYPE == 'pre_receive':
        ret_code = pre_receive(PLUGINS)
        sys.exit(1 if DEBUG_PRE_RECEIVE else ret_code)
    elif HOOK_TYPE == 'update':
        ret_code = update(PLUGINS)
        sys.exit(1 if DEBUG_UPDATE else ret_code)
    elif HOOK_TYPE == 'post_receive':
        ret_code = post_receive(PLUGINS)
        sys.exit(1 if DEBUG_POST_RECEIVE else ret_code)
