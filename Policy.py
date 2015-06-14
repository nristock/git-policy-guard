class Policy:
    def check(self, logger, ref_name, old_rev, new_rev, rev_list):
        raise NotImplementedError

    def name(self):
        raise NotImplementedError
