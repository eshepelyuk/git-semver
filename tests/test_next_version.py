from pathlib import Path


from git_semver import ERR_NOT_A_REPO, DEFAULT_PREFIX
from git_semver.main import git_semver, prefixed_version


from . import git_repo, git_empty_repo, CUSTOM_PREFIX, click_runner


def test_not_git_repo(click_runner):
    result = click_runner.invoke(git_semver)

    assert result.exit_code == ERR_NOT_A_REPO
    assert 'fatal: Not a git repository' in result.stderr


def test_print_current_empty_git_repo(click_runner):
    git_empty_repo(Path.cwd())
    result = click_runner.invoke(git_semver)

    assert result.exit_code == 0
    assert "0.0.0" in result.stdout
    assert result.stderr is ''

    result = click_runner.invoke(git_semver, ["-p", "qqq-"])

    assert result.exit_code == 0
    assert "qqq-0.0.0" in result.stdout
    assert result.stderr is ''


def test_print_current_tagged_git_repo(click_runner):
    git_repo(Path.cwd())

    result = click_runner.invoke(git_semver)

    assert result.exit_code == 0
    assert "1.1.1" in result.stdout

    result = click_runner.invoke(git_semver, ["-p", "aaa-"])

    assert result.exit_code == 0
    assert f"{CUSTOM_PREFIX}-2.2.2" in result.stdout


def test_next_patch(click_runner):
    git_repo(Path.cwd())

    result = click_runner.invoke(git_semver, ["-n", "patch"])

    assert result.exit_code == 0
    assert "1.1.2" in result.stdout

    result = click_runner.invoke(git_semver, ["-p", f"{CUSTOM_PREFIX}-", "-n", "patch"])

    assert result.exit_code == 0
    assert f"{CUSTOM_PREFIX}-2.2.3" in result.stdout


def test_next_minor(click_runner):
    git_repo(Path.cwd())

    result = click_runner.invoke(git_semver, ["-n", "minor"])

    assert result.exit_code == 0
    assert "v1.2.0" in result.stdout

    result = click_runner.invoke(git_semver, ["-p", f"{CUSTOM_PREFIX}-", "-n", "minor"])

    assert result.exit_code == 0
    assert f"{CUSTOM_PREFIX}-2.3.0" in result.stdout


def test_next_major(click_runner):
    git_repo(Path.cwd())

    result = click_runner.invoke(git_semver, ["-n", "major"])

    assert result.exit_code == 0
    assert "v2.0.0" in result.stdout

    result = click_runner.invoke(git_semver, ["-p", f"{CUSTOM_PREFIX}-", "-n", "major"])

    assert result.exit_code == 0
    assert f"{CUSTOM_PREFIX}-3.0.0" in result.stdout

def test_empty_prefix(click_runner):
    r = git_repo(Path.cwd())
    r.git.tag("-a", "-m", "chore: release", f"1.1.1")

    r.git.commit("--allow-empty", "-m", "msg2")
    r.git.tag("-a", "-m", "chore: release", f"{CUSTOM_PREFIX}2.2.3")

    result = click_runner.invoke(git_semver, ["-p", "",])
    assert "1.1.1" in result.stdout

    result = click_runner.invoke(git_semver, ["-p", "", "-n", "patch"])
    assert "1.1.2" in result.stdout


def test_multiple_branches(click_runner):
    r = git_repo(Path.cwd())

    r.git.commit("--allow-empty", "-m", "commit2")
    r.git.tag("-a", "-m", "chore: release", prefixed_version("1.2.0"))

    r.git.commit("--allow-empty", "-m", "commit3")
    r.git.tag("-a", "-m", "chore: release", prefixed_version("1.3.0"))

    result = click_runner.invoke(git_semver)
    assert prefixed_version("1.3.0") in result.stdout

    r.git.checkout("-b", "fix_branch_1_2_0", prefixed_version("1.2.0"))

    result = click_runner.invoke(git_semver)
    assert prefixed_version("1.2.0") in result.stdout

    result = click_runner.invoke(git_semver, ["-n", "minor"])
    assert prefixed_version("1.3.0") in result.stdout
