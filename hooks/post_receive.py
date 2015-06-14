import sys

from Plugin import RefUpdateInfo


def execute(plugins):
    received_refs = []

    for line in sys.stdin:
        ref_info = line.strip().split(' ')
        received_refs += [RefUpdateInfo(ref_info[2], ref_info[0], ref_info[1])]

    for plugin in plugins:
        plugin.post_receive(received_refs)

    return 0
