import unittest

from Utils import GitReference


def make_ref(ref_type, name):
    return 'refs/{0}/{1}'.format(ref_type, name)


def make_branch_ref(name):
    return make_ref('heads', name)


def make_tag_ref(name):
    return make_ref('tags', name)


class GitReferenceTests(unittest.TestCase):
    def test_branch(self):
        branch_name = 'my-awesome-branch'

        git_ref = GitReference(make_branch_ref(branch_name))
        self.assertTrue(git_ref.is_branch())
        self.assertFalse(git_ref.is_remote())
        self.assertFalse(git_ref.is_tag())
        self.assertEqual(git_ref.name, branch_name)

    def test_tag(self):
        tag_name = 'v1.0.0'

        git_ref = GitReference(make_tag_ref(tag_name))
        self.assertTrue(git_ref.is_tag())
        self.assertFalse(git_ref.is_branch())
        self.assertFalse(git_ref.is_remote())
        self.assertEqual(git_ref.name, tag_name)
