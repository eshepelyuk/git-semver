from pathlib import Path

import pytest
from click.testing import CliRunner
from git import Repo
from git_semver import DEFAULT_PREFIX

CUSTOM_PREFIX = "aaa"


def git_empty_repo(path):
    return Repo.init(path)


def git_repo(path):
    r = git_empty_repo(path)

    r.git.commit("--allow-empty", "-m", "initial")

    r.git.tag("-a", "-m", "chore: release", f"{DEFAULT_PREFIX}1.1.1")
    r.git.tag("-a", "-m", "chore: release", f"{CUSTOM_PREFIX}-2.2.2")

    return r


@pytest.fixture()
def click_runner():
    runner = CliRunner(mix_stderr=False)
    with runner.isolated_filesystem():
        yield runner
