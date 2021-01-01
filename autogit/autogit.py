import os
import os.path as osp
import subprocess
from datetime import datetime


branch_dir = osp.abspath(osp.join(osp.dirname(__file__), '..'))
print(branch_dir)

print(subprocess.run('pwd', cwd=branch_dir))
assert osp.exists(osp.join(branch_dir, '.git')), 'Could not find .git'


current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=branch_dir, capture_output=True)
branch_name = current_branch.stdout.strip().decode('UTF-8')
print(branch_dir, branch_name)
backup_branch_name = f'{branch_name}-backup'

# git branch --list <backupbranch>
backup_exists = subprocess.run(['git', 'branch', '--list', backup_branch_name], cwd=branch_dir, capture_output=True)
if len(backup_exists.stdout) == 0:
    print('Creating backup branch')
    # git branch <backupbranch>
    backup_exists = subprocess.run(['git', 'branch', backup_branch_name], cwd=branch_dir, capture_output=True)

_ = subprocess.run(['git', 'add', '-A'], cwd=branch_dir, capture_output=True)
print(_)
_ = subprocess.run(['git', 'commit', '--allow-empty', '--allow-empty-message', '-m', '""'], cwd=branch_dir, capture_output=True)
print(_)
_ = subprocess.run(['git', 'checkout', backup_branch_name], cwd=branch_dir, capture_output=True)
print(_)
_ = subprocess.run(['git', 'checkout', branch_name, '.'], cwd=branch_dir, capture_output=True)
print(_)
_ = subprocess.run(['git', 'add', '-A'], cwd=branch_dir, capture_output=True)
print(_)
timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
_ = subprocess.run(['git', 'commit', '-m', f'Backup: {timestamp}'], cwd=branch_dir, capture_output=True)
print(_)
_ = subprocess.run(['git', 'checkout', branch_name], cwd=branch_dir, capture_output=True)
print(_)
_ = subprocess.run(['git', 'reset', 'HEAD^'], cwd=branch_dir, capture_output=True)
print(_)
