import os
import os.path as osp
import subprocess
from datetime import datetime
import functools


def backup(path_to_repository, include_untracked=True, verbose=True):
    """
    Arguments:
        path_to_repository (str): A path (potentially relative) to the git repository
        verbose (bool): Print debug information
        include_untracked (bool): If true, this will include files that are not
            currently tracked by git as well. It still respects .gitignore though
            Otherwise, only files that are being tracked by git will be logged.
    """

    untracked_flag = '-A' if include_untracked else '-u'

    branch_dir = osp.abspath(path_to_repository)
    assert osp.exists(osp.join(branch_dir, '.git')), 'Could not find .git'
    
    git_run = functools.partial(subprocess.run, cwd=branch_dir, capture_output=True, encoding='UTF-8')

    # Get current branch name with
    # git rev-parse --abbrev-ref HEAD
    current_branch = git_run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch_name = current_branch.stdout.strip()
    # Backing up to {branch_name}-backup (e.g. master-backup) 
    backup_branch_name = f'{branch_name}-backup'

    if verbose:
        print(f'Backing up {branch_name} to {backup_branch_name} on repo {branch_dir}')

    # git branch --list <backupbranch>
    backup_exists = git_run(['git', 'branch', '--list', backup_branch_name])
    if len(backup_exists.stdout) == 0:
        if verbose:
            print('Creating backup branch')
        # git branch <backupbranch>
        git_run(['git', 'branch', backup_branch_name])

    commands = []
    commands.append(git_run(['git', 'add', untracked_flag]))
    commands.append(git_run(['git', 'commit', '--allow-empty', '--allow-empty-message', '-m', '']))
    commands.append(git_run(['git', 'checkout', backup_branch_name]))
    commands.append(git_run(['git', 'checkout', branch_name, '.']))
    commands.append(git_run(['git', 'add', untracked_flag]))
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    commands.append(git_run(['git', 'commit', '-m', f'Backup: {timestamp}']))
    backup_id = commands[-1].stdout.split('\n')[0]
    if 'nothing to commit' in commands[-1].stdout:
        backup_id = None
        if verbose:
            print('There was no change since the last backup. No commit being created')
    commands.append(git_run(['git', 'checkout', branch_name]))
    commands.append(git_run(['git', 'reset', 'HEAD^']))
    if verbose:
        import textwrap
        for command in commands:
            print(' '.join(command.args))
            print(textwrap.indent((command.stdout + command.stderr), '\t'))
    return backup_id

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path")
    parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("--only-tracked", help="Only backup files that have previously been added to git",
                action="store_true")
    args = parser.parse_args()

    print(backup(args.repo_path, include_untracked=not args.only_tracked, verbose=args.verbose))

if __name__ == '__main__':
    main()