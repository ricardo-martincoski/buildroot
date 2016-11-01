#!/usr/bin/env python
# this script conforms to pyflakes && pep8 --ignore=E501

import os
import subprocess


def get_absolute_path(path=os.path.dirname(os.path.realpath(__file__))):
    return os.path.realpath(path)


def change_dir_to(path):
    os.chdir(path)


# using old-style class so this script can be run in a plain vanilla CentOS 5 using python 2.4.3
class Utilities(object):
    commit_data = 10000
    # debug intentionally left on. It pollutes the test log but it shows relevant info when a test fails
    # TODO allow setting this at command line
    verbose = 0

    def run_commands_or_exit(self, commands):
        for command in commands:
            if self.verbose >= 2:
                print('%s' % command)
            result = os.system(command)
            if result != 0:
                raise OSError("command '%s' failed with error %d" % (command, result / 256))

    def exit_if_the_patch_instrumenting_the_source_code_is_not_present(self):
        self.run_commands_or_exit(
            ['grep -q "Checked out" support/download/git'])

    def exit_if_user_cannot_run_command_in_localhost_through_ssh_without_password_prompt(self):
        self.run_commands_or_exit(
            ['ssh localhost true'])

    def create_a_fake_package(self, remote_url_of_local_repo):
        self.run_commands_or_exit(
            ['mkdir package/package',
             'echo "PACKAGE_VERSION = invalid" >> package/package/package.mk',
             'echo "PACKAGE_SITE = %s/package.git" >> package/package/package.mk' % remote_url_of_local_repo,
             'echo "PACKAGE_SITE_METHOD = git" >> package/package/package.mk',
             'echo \'$(eval $(generic-package))\' >> package/package/package.mk'])

    def create_a_config_file(self):
        self.run_commands_or_exit(
            ['make defconfig >/dev/null 2>/dev/null',
             'echo \'BR2_DL_DIR="$(TOPDIR)/package/package/dl"\' >> .config',
             'echo \'BR2_BACKUP_SITE=""\' >> .config',
             'make oldconfig >/dev/null 2>/dev/null'])

    def exit_if_temporary_files_already_exist(self):
        if not os.path.isfile('support/download/git'):
            raise OSError('These tests must be run from Buildroot base dir')
        if os.path.isfile('.config'):
            raise OSError('File .config should not exist')
        if os.path.isfile('stdout'):  # FIXME ugly abstraction error, but it does the job
            raise OSError('File stdout should not exist')
        if os.path.isdir('package/package/'):
            raise OSError('The fake package package/package/ should not exist')

    def remove_temporary_files(self):
        self.run_commands_or_exit(
            ['rm -rf package/package/',
             'rm -f .config',
             'rm -f stdout'])

    def remove_dowloaded_tarball(self):
        self.run_commands_or_exit(
            ['rm -rf package/package/dl'])

    def run_commands_or_fail(self, commands):
        for command in commands:
            if self.verbose >= 2:
                print('%s' % command)
            result = os.system(command)
            # FIXME ugly abstraction error, but it does the job
            self.assertEqual(0, result, "command %s failed with error %d" % (command, result / 256))

    def create_test_repo(self):
        self.run_commands_or_fail(
            ['git init -q package/package/package.git'])

    def remove_test_repo(self):
        self.run_commands_or_fail(
            ['rm -rf package/package/package.git'])

    def create_commit_in_test_repo(self):
        base_dir = os.path.realpath('.')
        os.chdir('package/package/package.git')
        self.run_commands_or_fail(
            ['echo %i > %i' % (self.commit_data, self.commit_data),
             'git add %i' % self.commit_data,
             'git commit -q -m %i' % self.commit_data])
        self.commit_data += 1
        sha1 = self.get_sha1_from_checkout()
        os.chdir(base_dir)
        return sha1

    def checkout_a_new_branch_in_test_repo(self, branch):
        base_dir = os.path.realpath('.')
        os.chdir('package/package/package.git')
        self.run_commands_or_fail(
            ['git branch -f "%s" >/dev/null' % branch,
             'git checkout -q -f "%s"' % branch])
        os.chdir(base_dir)

    def create_a_special_ref_in_test_repo(self, special_ref):
        base_dir = os.path.realpath('.')
        os.chdir('package/package/package.git')
        directory = '/'.join(special_ref.split('/')[:-1])
        self.run_commands_or_fail(
            ['git branch -f temporary >/dev/null',
             'mkdir -p .git/refs/%s' % directory,
             'mv .git/refs/heads/temporary .git/refs/%s' % special_ref])
        os.chdir(base_dir)

    def create_a_new_tag_in_test_repog(self, tag):
        base_dir = os.path.realpath('.')
        os.chdir('package/package/package.git')
        self.run_commands_or_fail(
            ['git tag -a "%s" -m "%s"' % (tag, self.commit_data)])
        self.commit_data += 1
        os.chdir(base_dir)

    def download_source_using_buildroot(self, version, extra_options=''):
        redirect_stderr = '2>/dev/null'
        if self.verbose >= 1:
            os.system('echo; cd package/package/package.git && GIT_PAGER= git log --all --graph --abbrev-commit --pretty=oneline --decorate && git ls-remote .')
            redirect_stderr = ''
        # Using 'make PACKAGE_VERSION=' does not work for references with slash, so write to the .mk
        self.run_commands_or_fail(
            ['sed -e \'s#^PACKAGE_VERSION.*$#PACKAGE_VERSION = %s#g\' -i package/package/package.mk' % version])
        result = os.system(
            'make %s package-dirclean package-source >stdout %s' % (extra_options, redirect_stderr))
        if self.verbose >= 1:
            os.system('echo -; cat stdout; echo -')
        return result

    def check_tarball_exists(self, expected_download):
        if self.verbose >= 1:
            os.system('echo -n "dl: " ; ls package/package/dl/')
        return os.path.isfile('package/package/dl/package-' + expected_download + '.tar.gz')

    def get_sha1_from_checkout(self):
        pipe = subprocess.Popen("git rev-parse HEAD", shell=True, stdout=subprocess.PIPE)
        # use .decode() to be compatible to python 3 which returns bytesliteral
        sha1 = pipe.communicate()[0].decode().strip()
        if len(sha1) != 40:
            raise OSError("Failed to create commit, got sha1 '%s'" % sha1)
        return sha1

    def check_sha1_appeared_in_build_log(self, sha1):  # it needs some instrumentation in the code
        self.run_commands_or_fail(
            ['grep -q "Checked out \'%s\'" stdout' % sha1])

    def check_in_the_build_log_if_a_shallow_fetch_was_enough(self):  # it is very coupled to the source code
        if 0 == os.system('grep -q "Doing full" stdout'):
            return False
        if 0 == os.system('grep -q "Doing shallow fetch of all branches" stdout'):
            return False
        return True

    def detach_head_in_test_repo(self):
        base_dir = os.path.realpath('.')
        os.chdir('package/package/package.git')
        self.run_commands_or_fail(
            ['git checkout -q -f HEAD~0'])
        os.chdir(base_dir)

    def checkout_branch_in_test_repo(self, branch):
        base_dir = os.path.realpath('.')
        os.chdir('package/package/package.git')
        self.run_commands_or_fail(
            ['git checkout -q -f "%s"' % branch])
        os.chdir(base_dir)

    def create_a_submodule(self, submodule, remote_url_of_local_repo):
        base_dir = os.path.realpath('.')
        submodule_dir = 'package/package/%s.git' % submodule
        self.run_commands_or_fail(
            ['git init -q %s' % submodule_dir])
        os.chdir(submodule_dir)
        self.run_commands_or_fail(
            ['echo %s > %s' % (submodule, submodule),
             'git add %s' % submodule,
             'git commit -q -m %s' % submodule])
        os.chdir(base_dir)
        os.chdir('package/package/package.git')
        self.run_commands_or_fail(
            ['git submodule add %s/%s.git ./%s 2>/dev/null' % (remote_url_of_local_repo, submodule, submodule),
             'echo %i > %i' % (self.commit_data, self.commit_data),
             'git add %i' % self.commit_data,
             'git commit -q -m %i' % self.commit_data])
        self.commit_data += 1
        sha1 = self.get_sha1_from_checkout()
        os.chdir(base_dir)
        return sha1

    def check_tarball_contains_the_submodule(self, expected_download, submodule):
        if self.verbose >= 1:
            os.system('echo "tar:"; tar -tf "package/package/dl/package-%s.tar.gz"' % expected_download)
        return 0 == os.system('tar -tf "package/package/dl/package-%s.tar.gz" | grep -q "%s/%s"' % (expected_download, submodule, submodule))

    def create_commit_with_ambiguous_short_sha1_in_test_repo(self):
        base_dir = os.path.realpath('.')
        os.chdir('package/package/package.git')
        # The shortest partial sha1 that git commands accept are 4 hexa long, so
        # creating at most 2^4+1=65537 commits creates an ambiguous short sha1.
        # NOTICE we don't need the sha1 of the commit to be ambiguous to a
        # commit-ish sha1. This makes this test possible in much fewer steps
        # than 2^4+1 commits (in the order of seconds using space of order of
        # MiBs instead of taking minutes and GiBs that would be needed to
        # garantee 2 ambiguous commit-ish sha1).
        os.system('for i in $(seq 100000 165537) ; do'
                  '  echo $i>$i;'
                  '  git add $i;'
                  '  git commit -q -m $i;'
                  '  if ! git rev-parse -q $(git rev-parse HEAD | head -c 4)'
                  '      2>&1 >/dev/null ; then'
                  '    break;'
                  '  fi;'
                  'done')
        self.run_commands_or_fail(
            ['git checkout $(git rev-parse HEAD | head -c 4) 2>&1 | grep -q ambiguous'])
        sha1 = self.get_sha1_from_checkout()
        print("sha1: %s" % sha1)
        os.chdir(base_dir)
        return sha1[:4]
