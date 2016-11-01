#!/usr/bin/env python
# this script conforms to pyflakes && pep8 --ignore=E501

import git_util
import unittest


class Keywords(unittest.TestCase, git_util.Utilities):
    def given_there_is_a_commit_pointed_only_by_the_branch_named(self, branch):
        self.checkout_a_new_branch_in_test_repo(branch)
        sha1 = self.create_commit_in_test_repo()
        return sha1

    def given_the_same_commit_is_pointed_by_the_branch_named(self, branch):
        self.checkout_a_new_branch_in_test_repo(branch)

    def given_there_is_another_commit_in_the_upstream(self):
        sha1 = self.create_commit_in_test_repo()
        return sha1

    def given_there_is_a_commit_pointed_only_by_the_tag_named(self, tag):
        sha1 = self.create_commit_in_test_repo()
        self.create_a_new_tag_in_test_repog(tag)
        self.create_commit_in_test_repo()
        return sha1

    def given_there_is_a_commit_pointed_only_by_the_special_ref_named(self, special_ref):
        self.detach_head_in_test_repo()
        sha1 = self.create_commit_in_test_repo()
        self.create_a_special_ref_in_test_repo(special_ref)
        self.checkout_branch_in_test_repo("master")
        return sha1

    def given_there_is_a_commit_with_ambiguous_partial_sha1(self):
        partial_sha1 = self.create_commit_with_ambiguous_short_sha1_in_test_repo()
        return partial_sha1

    def given_the_commits_are_not_the_same(self, sha1_1st, sha1_2nd):
        self.assertNotEqual(sha1_1st, sha1_2nd)

    def given_the_commits_are_the_same(self, sha1_1st, sha1_2nd):
        self.assertEqual(sha1_1st, sha1_2nd)

    def when_i_download_the_version(self, version):
        result = self.download_source_using_buildroot(version)
        self.assertEqual(0, result, "download of version %s failed" % version)

    def when_i_download_with_support_to_git_modules_the_version(self, version):
        result = self.download_source_using_buildroot(version, 'PACKAGE_GIT_SUBMODULES=YES')
        self.assertEqual(0, result, "download with support to git modules of version %s failed" % version)

    def then_i_can_see_the_tarball_exists(self, version):
        result = self.check_tarball_exists(version)
        self.assertTrue(result, "Tarball for version %s does not exist" % version)

    def then_i_can_see_the_tarball_contains_the_submodule(self, version, submodule):
        result = self.check_tarball_contains_the_submodule(version, submodule)
        self.assertTrue(result, "Tarball does not contain the submodule data")

    def then_i_can_see_the_tarball_does_not_contain_the_submodule(self, version, submodule):
        result = self.check_tarball_contains_the_submodule(version, submodule)
        self.assertFalse(result, "Tarball does contain the submodule data, but it shouldn't")

    def then_i_can_see_the_downloaded_sha1_is(self, sha1):
        self.check_sha1_appeared_in_build_log(sha1)

    def then_i_can_see_a_shallow_fetch_was_enough(self):
        result = self.check_in_the_build_log_if_a_shallow_fetch_was_enough()
        self.assertTrue(result, "A shallow fetch was not enough")

    def then_i_can_see_a_shallow_fetch_was_not_enough(self):
        result = self.check_in_the_build_log_if_a_shallow_fetch_was_enough()
        self.assertFalse(result, "A shallow fetch was enough")

    def given_there_is_a_submodule_named(self, submodule, remote_url_of_local_repo):
        self.create_a_submodule(submodule, remote_url_of_local_repo)
