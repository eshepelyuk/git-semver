from pathlib import Path

from git_semver import ERR_NOT_A_REPO, DEFAULT_PREFIX
from git_semver.main import git_semver, prefixed_version as pf

from . import git_repo, git_empty_repo, click_runner
from git import Repo

def test_add_tag_empty_repo(click_runner):
    r = git_empty_repo(Path.cwd())
    r.git.commit("--allow-empty", "-m", "initial")

    assert r.tags == []

    result = click_runner.invoke(git_semver, ["-T"])

    assert result.exit_code == 0
    assert result.stderr is ''
    assert pf("0.0.0") in result.stdout
    assert r.git.tag() == pf("0.0.0")

    result = click_runner.invoke(git_semver, ["-T", "-n", "patch"])

    assert result.exit_code == 0
    assert result.stderr is ''
    assert pf("0.0.1") in result.stdout
    assert str(r.tags[-1]) == pf("0.0.1")


def test_add_tag_has_tag(click_runner):
    r = git_repo(Path.cwd())
    assert [str(t) for t in r.tags if str(t).startswith(DEFAULT_PREFIX)] == [pf("1.1.1")]

    result = click_runner.invoke(git_semver, ["-T"])
    assert result.exit_code == ERR_NOT_A_REPO
    assert result.stdout == ''
    assert 'fatal: unable to create tag' in result.stderr
    assert [str(t) for t in r.tags if str(t).startswith(DEFAULT_PREFIX)] == [pf("1.1.1")]

    result = click_runner.invoke(git_semver, ["-T", "-n", "patch"])

    assert result.exit_code == 0
    assert result.stderr is ''
    assert pf("1.1.2") in result.stdout
    assert [str(t) for t in r.tags if str(t).startswith(DEFAULT_PREFIX)] == [pf("1.1.1"), pf("1.1.2")]

def test_push_tag(click_runner, tmp_path):
    remote = git_repo(tmp_path)

    Repo.clone_from(tmp_path, Path.cwd())

    result = click_runner.invoke(git_semver, ["-TU", "-n", "patch"])
    assert result.exit_code == 0
    assert result.stderr is ''

    assert [str(t) for t in remote.tags if str(t).startswith(DEFAULT_PREFIX)] == [pf("1.1.1"), pf("1.1.2")]
