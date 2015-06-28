from itertools import groupby
import os
import subprocess
import re


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

    def is_null_rev(self):
        reduced_name = ''.join(ch for ch, _ in groupby(self.rev))
        return reduced_name == '0'


class GitReference:
    REF_INFO_REGEX = re.compile(r'refs/(.*)/(.*)')

    def __init__(self, ref):
        self.ref = ref
        (self.type, self.name) = GitReference.parse_ref_info(ref)

    @staticmethod
    def parse_ref_info(ref):
        ref_info = GitReference.REF_INFO_REGEX.match(ref)
        return ref_info.group(1), ref_info.group(2)

    def is_branch(self):
        return self.type == 'heads'

    def is_tag(self):
        return self.type == 'tags'

    def is_remote(self):
        return self.type == 'remotes'
