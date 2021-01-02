import os
import os.path as osp
import subprocess
from datetime import datetime
import functools


def backup(path_to_repository, verbose=True):
    branch_dir = path_to_repository
    assert osp.exists(osp.join(branch_dir, '.git')), 'Could not find .git'
    
    git_run = functools.partial(subprocess.run, cwd=branch_dir, capture_output=True)

    # Get current branch name with
    # git rev-parse --abbrev-ref HEAD
    current_branch = git_run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch_name = current_branch.stdout.strip().decode('UTF-8')
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
    commands.append(git_run(['git', 'add', '-A']))
    commands.append(git_run(['git', 'commit', '--allow-empty', '--allow-empty-message', '-m', '""']))
    commands.append(git_run(['git', 'checkout', backup_branch_name]))
    commands.append(git_run(['git', 'checkout', branch_name, '.']))
    commands.append(git_run(['git', 'add', '-A']))
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    commands.append(git_run(['git', 'commit', '-m', f'Backup: {timestamp}']))
    if 'nothing to commit' in commands[-1].stdout.decode('UTF-8'):
        if verbose:
            print('There was no change since the last backup. No commit being created')
    commands.append(git_run(['git', 'checkout', branch_name]))
    commands.append(git_run(['git', 'reset', 'HEAD^']))
    if verbose:
        for command in commands:
            print(command)

if __name__ == '__main__':
    backup(osp.abspath(osp.join(osp.dirname(__file__), '..')), verbose=True)
