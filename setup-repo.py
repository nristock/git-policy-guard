#!/bin/env python3
import argparse
import os
import stat

from TermColors import AnsiColor

HOOK_DIR = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument('hook_dir', type=str, help="Directory in which to create the hook scripts", default=HOOK_DIR,
                    nargs='?')
parser.add_argument('--no-pre-receive', '-a', help="Don't create pre-receive hook", action='store_false', default=True,
                    dest='pre_receive')
parser.add_argument('--no-update', '-u', help="Don't create update hook", action='store_false', default=True,
                    dest='update')
parser.add_argument('--no-post-receive', '-z', help="Don't create post-receive hook", action='store_false',
                    default=True, dest='post_receive')

args = parser.parse_args()

HOOK_DIR = args.hook_dir
HOOK_DIR_NAME = os.path.basename(HOOK_DIR)
POLICY_GUARD_INSTALL_DIR = "$GIT_DIR/{0}/git-policy-guard".format(HOOK_DIR_NAME)

print(AnsiColor.colorize(
    "$BLUE$Creating hooks in $YELLOW${0}$BLUE$ with main script in $YELLOW${1}$BLUE$".format(HOOK_DIR,
                                                                                             POLICY_GUARD_INSTALL_DIR)))

hook_commands = {
    'pre-receive': 'python3 "{0}/policy_guard.py" pre_receive <&0'.format(POLICY_GUARD_INSTALL_DIR),
    'update': 'python3 "{0}/policy_guard.py" update $1 $2 $3'.format(POLICY_GUARD_INSTALL_DIR),
    'post-receive': 'python3 "{0}/policy_guard.py" post_receive <&0'.format(POLICY_GUARD_INSTALL_DIR)
}


def create_hook(hook_name):
    target_file = os.path.join(HOOK_DIR, hook_name)
    if os.path.isfile(target_file):
        print(AnsiColor.colorize(
            "$RED$Not creating $MAGENTA${0}$RED$ hook script: File already exists".format(hook_name)))
        return

    with open(target_file, 'w+') as hook_file:
        print(AnsiColor.colorize("$BLUE$Creating $GREEN${0}$BLUE$ hook script".format(hook_name)))
        hook_file.write("#!/bin/bash\n{0}".format(hook_commands[hook_name]))
        os.chmod(target_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)


if args.pre_receive:
    create_hook('pre-receive')

if args.update:
    create_hook('update')

if args.post_receive:
    create_hook('post-receive')
