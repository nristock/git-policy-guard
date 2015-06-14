class RefUpdateInfo:
    def __init__(self, ref_name, old_rev, new_rev):
        self.ref_name = ref_name
        self.old_rev = old_rev
        self.new_rev = new_rev


class Plugin:
    def pre_receive(self, ref_updates):
        """Git pre-receive hook callback for a plugin.
            Args:
                ref_updates (list[RefUpdateInfo]): A list of all refs to be updated including the old and new revisions
        """
        return True

    def update(self, ref_update_info):
        """Git update hook callback for a plugin.
            Args:
                ref_update_info (RefUpdateInfo): The ref being updated including the old and new revisions
        """
        return True

    def post_receive(self, updated_refs):
        """Git post-recieve hook callback for a plugin.
            Args:
                updated_refs (list[RefUpdateInfo]): A list of all updated refs including the old and new revisions
        """
        return True
