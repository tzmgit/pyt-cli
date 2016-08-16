"""Tests for our `pyt gid` subcommand."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase


class TestGid(TestCase):

    def test_append_id(self):
        out_file = './data/test_gid_append_result.txt'
        output = popen(['pyt', 'gid', './data/test_gid_append.txt', 't.', '--append', '--output=' + out_file], stdout=PIPE).communicate()[0]
        print output
        with open(out_file) as f:
            lines = f.readlines()
            self.assert_("{'t.a': 3, 't.b': 2}\n" in lines)
            self.assert_("t.b.002 b\n" in lines)

    def test_non_append_id(self):
        out_file = './data/test_gid_result.txt'
        output = popen(['pyt', 'gid', './data/test_gid.txt', 't.', '--output=' + out_file], stdout=PIPE).communicate()[0]
        print output
        with open(out_file) as f:
            lines = f.readlines()
            self.assert_("{'t.a': 3, 't.b': 2}\n" in lines)
