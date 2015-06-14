import sys

from Logging import get_main_logger
from Plugin import RefUpdateInfo
from PluginError import PluginError


def execute(plugins):
    ref_updates = []
    for line in sys.stdin:
        ref_info = line.split(' ')
        ref_updates += [RefUpdateInfo(ref_info[2], ref_info[0], ref_info[1])]

    for plugin in plugins:
        try:
            plugin.pre_receive(ref_updates)
        except PluginError as err:
            logger = get_main_logger()
            logger.error(err.message)

            if err.stop_operation:
                return 1

    return 0
