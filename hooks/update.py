import sys

from Logging import get_main_logger
from Plugin import RefUpdateInfo
from PluginError import PluginError


def execute(plugins):
    ref_name = sys.argv[2]
    old_rev = sys.argv[3]
    new_rev = sys.argv[4]

    for plugin in plugins:
        try:
            plugin.update(RefUpdateInfo(ref_name, old_rev, new_rev))
        except PluginError as err:
            logger = get_main_logger()
            logger.error(err.message)

            if err.stop_operation:
                return 1

    return 0
