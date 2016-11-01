#!/usr/bin/env python
# this script conforms to pyflakes && pep8 --ignore=E501

# BEFORE calling this script, make sure:
# - there is a ssh server installed
# - there is a key pair generated that allow the current user to run 'ssh localhost' without being prompted for entering a password

# TODO test recursive submodules
# TODO test another transport protocols: git, https, ... - need manual setup of git server
# TODO test extra download options, especially --reference
# TODO test which cases should have optimized download, and which cases use the full fetch


import git_util
import git_keywords
import unittest

pwd = git_util.get_absolute_path()
buildroot_base_dir = pwd + '/../../../'
# use .decode() to be compatible to python 3 which returns bytesliteral
remote_url_of_local_repo = 'ssh://localhost/%s/package/package' % buildroot_base_dir


class TestSuiteSupportDownloadGitRefs(git_keywords.Keywords):
    # do not use setUpClass/tearDownClass because they need python 2.7
    def setUp(self):
        git_util.change_dir_to(buildroot_base_dir)
        self.exit_if_the_patch_instrumenting_the_source_code_is_not_present()
        self.exit_if_user_cannot_run_command_in_localhost_through_ssh_without_password_prompt()
        self.exit_if_temporary_files_already_exist()
        self.create_a_fake_package(remote_url_of_local_repo)
        self.create_a_config_file()
        self.create_test_repo()
        self.create_commit_in_test_repo()  # initial commit
        self.remove_dowloaded_tarball()

    def tearDown(self):
        self.remove_temporary_files()
        self.remove_test_repo()
        git_util.change_dir_to(pwd)

    def test101_tag_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature101")
        self.when_i_download_the_version("feature101")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("feature101")

    def test101b_tag_uses_optimized_download(self):
        # old git client (e.g. 1.7.1) does not fetch tag without {refs/,}tags/
        self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature101b")
        self.when_i_download_the_version("feature101b")
        self.then_i_can_see_the_tarball_exists("feature101b")
        self.then_i_can_see_a_shallow_fetch_was_enough()

    def test101c_tag_using_full_name_uses_optimized_download(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature101c")
        self.when_i_download_the_version("refs/tags/feature101c")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("refs_tags_feature101c")
        self.then_i_can_see_a_shallow_fetch_was_enough()

    def test102_tag_can_be_preferred_over_branch_by_using_full_name(self):
        tag_sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature102")
        branch_sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feature102")
        self.given_the_commits_are_not_the_same(branch_sha1, tag_sha1)
        self.when_i_download_the_version("refs/tags/feature102")
        self.then_i_can_see_the_downloaded_sha1_is(tag_sha1)
        self.then_i_can_see_the_tarball_exists("refs_tags_feature102")

    def test201_sha1_not_branch_head_but_in_a_branch_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feature201")
        sha1_head = self.given_there_is_another_commit_in_the_upstream()
        self.given_the_commits_are_not_the_same(sha1, sha1_head)
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)

    def test201b_sha1_not_branch_head_but_in_a_branch_does_not_use_optimized_download(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feature201")
        sha1_head = self.given_there_is_another_commit_in_the_upstream()
        self.given_the_commits_are_not_the_same(sha1, sha1_head)
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)
        self.then_i_can_see_a_shallow_fetch_was_not_enough()

    def test202_sha1_of_branch_head_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feature202")
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)

    def test203_partial_sha1_of_branch_head_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feature203")
        partial_sha1 = sha1[:20]
        self.when_i_download_the_version(partial_sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(partial_sha1)

    def test204_sha1_of_commit_pointed_by_a_tag_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature204")
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)

    def test204b_sha1_of_commit_pointed_by_a_tag_uses_optimized_download(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature204b")
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)
        self.then_i_can_see_a_shallow_fetch_was_enough()

    def test205_sha1_head_of_branch_with_slash_in_the_name_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feat/ure205")
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)

    def test206_sha1_not_branch_head_but_in_a_branch_with_slash_in_the_name_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feat/ure206")
        sha1_head = self.given_there_is_another_commit_in_the_upstream()
        self.given_the_commits_are_not_the_same(sha1, sha1_head)
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)

    def test207_partial_sha1_of_tagged_commit_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature207")
        partial_sha1 = sha1[:20]
        self.when_i_download_the_version(partial_sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(partial_sha1)

    def test208_sha1_of_special_ref_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_special_ref_named("changes/02/2/8")
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)

    def test209_sha1_of_merged_special_ref_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_special_ref_named("changes/02/2/9")
        self.given_the_same_commit_is_pointed_by_the_branch_named("feature209")
        self.when_i_download_the_version(sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(sha1)

    def test210_partial_sha1_of_special_ref_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_special_ref_named("changes/02/2/10")
        partial_sha1 = sha1[:20]
        self.when_i_download_the_version(partial_sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(partial_sha1)

    def test211_partial_sha1_of_merged_special_ref_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_special_ref_named("changes/02/2/11")
        self.given_the_same_commit_is_pointed_by_the_branch_named("feature211")
        sha1_head = self.given_there_is_another_commit_in_the_upstream()
        self.given_the_commits_are_not_the_same(sha1, sha1_head)
        partial_sha1 = sha1[:20]
        self.when_i_download_the_version(partial_sha1)
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists(partial_sha1)

    def test212_partial_ambiguous_sha1_cannot_be_used(self):
        partial_sha1 = self.given_there_is_a_commit_with_ambiguous_partial_sha1()
        self.when_i_download_the_version(partial_sha1)
        self.then_i_can_see_the_downloaded_sha1_is(partial_sha1)
        self.then_i_can_see_the_tarball_exists(partial_sha1)
        self.then_i_can_see_a_shallow_fetch_was_enough()

    def test301_special_ref_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_special_ref_named("changes/03/3/1")
        self.when_i_download_the_version("refs/changes/03/3/1")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("refs_changes_03_3_1")

    def test302_merged_special_ref_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_special_ref_named("changes/03/3/2")
        self.given_the_same_commit_is_pointed_by_the_branch_named("feature302")
        self.when_i_download_the_version("refs/changes/03/3/2")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("refs_changes_03_3_2")

    def test401_branch_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feature401")
        self.when_i_download_the_version("feature401")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("feature401")

    def test402_branch_is_preferred_over_tag(self):  # XXX behavior enforced by git clone / fetch / checkout
        tag_sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature402")
        branch_sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feature402")
        self.given_the_commits_are_not_the_same(branch_sha1, tag_sha1)
        self.when_i_download_the_version("feature402")
        self.then_i_can_see_the_downloaded_sha1_is(branch_sha1)
        self.then_i_can_see_the_tarball_exists("feature402")

    def test403_branch_with_slash_in_the_name_can_be_used(self):
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_branch_named("feat/ure403")
        self.when_i_download_the_version("feat/ure403")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("feat_ure403")

    def test501_tag_can_be_used_when_there_are_submodules_without_support_to_git_modules(self):
        self.given_there_is_a_submodule_named("submodule501", remote_url_of_local_repo)
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature501")
        self.when_i_download_the_version("feature501")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("feature501")
        self.then_i_can_see_the_tarball_does_not_contain_the_submodule("feature501", "submodule501")

    def test502_tag_can_be_used_when_there_are_submodules_with_support_to_git_modules(self):
        self.given_there_is_a_submodule_named("submodule502", remote_url_of_local_repo)
        sha1 = self.given_there_is_a_commit_pointed_only_by_the_tag_named("feature502")
        self.when_i_download_with_support_to_git_modules_the_version("feature502")
        self.then_i_can_see_the_downloaded_sha1_is(sha1)
        self.then_i_can_see_the_tarball_exists("feature502")
        self.then_i_can_see_the_tarball_contains_the_submodule("feature502", "submodule502")

    def test901_head_can_be_used(self):
        self.when_i_download_the_version("HEAD")
        self.then_i_can_see_the_tarball_exists("HEAD")


if __name__ == '__main__':
    # unittest.main(verbosity=) is only available in python 2.7
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSuiteSupportDownloadGitRefs)
    unittest.TextTestRunner(verbosity=2).run(suite)
