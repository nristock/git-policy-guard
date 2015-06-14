import os
import re

from Policy import Policy


class FileBlacklist(Policy):
    def __init__(self, pattern):
        self.pattern = []

        for patt in pattern:
            self.pattern += [re.compile(patt)]

    def check(self, logger, ref_name, old_rev, new_rev, rev_list):
        has_error = False

        for rev in rev_list:
            files = rev.changed_files()

            for file in files:
                file_name = os.path.basename(file)

                for pattern in self.pattern:
                    if pattern.match(file_name):
                        logger.error("$YELLOW${0}$RESET$ matches blacklisted pattern $YELLOW$'{1}'".format(file_name,
                                                                                                           pattern.pattern))
                        has_error = True

        return not has_error

    def name(self):
        return "FileBlacklist"
