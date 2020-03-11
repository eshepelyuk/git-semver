from pathlib import Path

import click
from git import Repo
from git.exc import GitCommandError
from semantic_version import Version

from . import ERR_NOT_A_REPO, DEFAULT_PREFIX


def get_current_version(repo, prefix):
    try:
        return Version(
            repo.git.describe('--abbrev=0', '--first-parent', '--match', f'{prefix}[[:digit:]]*').lstrip(prefix))
    except GitCommandError:
        return Version('0.0.0')


def prefixed_version(version, prefix=DEFAULT_PREFIX):
    return f'{prefix}{version}'


@click.command()
@click.option('-n', '--next', 'nxt', type=click.Choice(['patch', 'minor', 'major']), help="")
@click.option('-p', '--prefix', 'prefix', default=DEFAULT_PREFIX, help="")
@click.option('-T', '--tag-add', 'tag_add', is_flag=True, help="")
@click.option('-U', '--tag-push', 'tag_push', is_flag=True, help="")
def git_semver(nxt, prefix, tag_add, tag_push):
    """
    Help for this tool
    """

    try:
        repo = Repo(Path.cwd())
    except:
        click.echo("fatal: Not a git repository", err=True)
        exit(ERR_NOT_A_REPO)

    current_version = get_current_version(repo, prefix)

    if nxt is None:
        print_str = prefixed_version(current_version, prefix)
    else:
        nxt_version = current_version.next_patch()
        if nxt == 'minor':
            nxt_version = current_version.next_minor()
        elif nxt == 'major':
            nxt_version = current_version.next_major()

        print_str = prefixed_version(nxt_version, prefix)

    if tag_add:
        try:
            repo.git.tag('-a', '-m', f'chore: release {print_str}', print_str)
            if tag_push:
                repo.git.push('origin', print_str)
        except:
            click.echo("fatal: unable to create tag", err=True)
            exit(ERR_NOT_A_REPO)

    print(print_str)
