import os
import subprocess


class GitRev:
    def __init__(self, rev):
        self.rev = rev

    def commit_message(self):
        command = 'git cat-file commit {0}'.format(self.rev).split(' ')
        git_cat_file = subprocess.Popen(command, env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = git_cat_file.communicate()
        stdout_str = bytes.decode(stdout)
        return stdout_str[stdout_str.index('\n\n') + 2:]

    def changed_files(self):
        command = 'git log -1 --name-only --pretty=format: {0}'.format(self.rev).split(' ')
        git_fil_list = subprocess.Popen(command, env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = git_fil_list.communicate()
        return filter(lambda x: x, bytes.decode(stdout).split('\n'))

    def hash(self):
        return self.rev
