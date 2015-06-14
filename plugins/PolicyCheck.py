import os
import subprocess

from Logging import get_main_logger, create_policy_logger
from Plugin import Plugin
from PluginError import PluginError
from Utils import GitRev


class PolicyCheck(Plugin):
    def __init__(self, policies):
        self.policies = policies

    def update(self, ref_update_info):
        log = get_main_logger()
        old_rev = ref_update_info.old_rev
        new_rev = ref_update_info.new_rev

        def get_pushed_revisions():
            command = 'git rev-list {0}..{1}'.format(old_rev, new_rev).split(' ')

            git_rev_list = subprocess.Popen(command, env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = git_rev_list.communicate()
            return list(map(lambda rev: GitRev(rev.strip()), filter(lambda x: x, bytes.decode(stdout).split('\n'))))

        pushed_revs = get_pushed_revisions()
        log.info("Evaluating commit policies for revisions $MAGENTA${0}$RESET$..$MAGENTA${1}".format(old_rev, new_rev))

        has_violations = False
        for policy in self.policies:
            name = policy.name()
            logger = create_policy_logger(name)
            if policy.check(logger, ref_update_info.ref_name, old_rev, new_rev, pushed_revs):
                log.info("$GREEN${0}: PASSED".format(name))
            else:
                has_violations = True
                log.error("$RED${0}: VIOLATION".format(name))

        if has_violations:
            raise PluginError(True, "$RED$At least one policy has been violated. Your push will be rejected.")

        log.info("All tests passed.")
