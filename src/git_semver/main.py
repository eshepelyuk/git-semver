from pathlib import Path

import click
from git import Repo
from git.exc import GitCommandError
from semantic_version import Version
import sys, traceback

from . import ERR_NOT_A_REPO, DEFAULT_PREFIX


def version_from_git(repo, prefix):
    try:
        v = repo.git.describe('--abbrev=0', '--match', f'{prefix}[[:digit:]]*')[len(prefix):]
        return Version(v)
    except GitCommandError:
        return Version('0.0.0')


def prefixed_version(version, prefix=DEFAULT_PREFIX):
    return f'{prefix}{version}'


@click.command()
@click.option('-e', '--current', 'current',
              help="SemVer compatible string used as a current VERSION. Disables detection from git repository tags.")
@click.option('-n', '--next', 'nxt', type=click.Choice(['patch', 'minor', 'major']),
              help="Generate new version, increasing one of current VERSION parts.")
@click.option('-N', '--next-debug', 'nxt_debug',
              is_flag=True, help="When used with -n/--next, also prints previous VERSION.")
@click.option('-p', '--prefix', 'prefix', default=DEFAULT_PREFIX, help="")
@click.option('-T', '--tag-add', 'tag_add', is_flag=True, help="Create annotated TAG in git repository, formatted as ${PREFIX}${VERSION}.")
@click.option('-U', '--tag-push', 'tag_push', is_flag=True, help="Push TAG created with -T/--tag-add option to git remote.")
@click.option('-d', '--debug', 'is_debug', is_flag=True, help="Enable verbose output, also enables exception stacktrace.")
@click.version_option()
def git_semver(current, nxt, nxt_debug, prefix, tag_add, tag_push, is_debug):
    """
This tool allows to enable language-agnostic `fileless` release pipeline for your projects
using `Git` as the only source of release metadata.
    """

    try:
        repo = Repo(Path.cwd())
    except:
        click.echo("fatal: Not a git repository", err=True)
        exit(ERR_NOT_A_REPO)

    current_version = version_from_git(repo, prefix) if current is None else Version(current)

    if nxt is None:
        print_str = prefixed_version(current_version, prefix)
    else:
        if nxt_debug:
            print(prefixed_version(current_version, prefix))

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
            if is_debug:
                traceback.print_exc(file=sys.stderr)
            click.echo("fatal: unable to create tag", err=True)
            exit(ERR_NOT_A_REPO)

    print(print_str)
