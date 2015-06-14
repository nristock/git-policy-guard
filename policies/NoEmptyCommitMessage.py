from Policy import Policy


class NoEmptyCommitMessage(Policy):
    def check(self, logger, ref_name, old_rev, new_rev, rev_list):
        for rev in rev_list:
            commit_message = rev.commit_message().strip()
            if not commit_message:
                logger.error("Found empty commit message in rev $YELLOW${0}".format(rev))
                return False

        return True

    def name(self):
        return "NoEmptyCommitMessage"
