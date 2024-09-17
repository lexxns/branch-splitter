import os

import pytest

from branch_splitter.git_repo import GitRepo


def test_get_current_branch(git_repo, temp_git_repo):
    _, default_branch = temp_git_repo
    assert git_repo.get_current_branch() == default_branch


def test_create_branch(git_repo):
    assert git_repo.create_branch('new_branch')
    assert git_repo.branch_exists('new_branch')


def test_get_changes(git_repo, temp_git_repo):
    _, default_branch = temp_git_repo
    changes = git_repo.get_changes('feature_branch', default_branch)
    assert len(changes) == 1
    assert changes[0]['file'] == 'initial_file.txt'
    assert changes[0]['message'] == 'Feature branch commit'
    assert 'Feature branch content' in changes[0]['diff']


def test_apply_change(git_repo, temp_git_repo):
    repo_path, default_branch = temp_git_repo
    changes = git_repo.get_changes('feature_branch', default_branch)
    git_repo.create_branch('test_branch')

    # Apply the change
    assert git_repo.apply_change(changes[0], 'test_branch')

    # Check if the change was applied
    repo = git_repo.repo
    repo.git.checkout('test_branch')
    with open(os.path.join(repo.working_dir, 'initial_file.txt'), 'r') as f:
        content = f.read()
    assert content == 'Feature branch content'

    # Try to apply the same change again (should return False)
    assert not git_repo.apply_change(changes[0], 'test_branch')


def test_branch_exists(git_repo, temp_git_repo):
    _, default_branch = temp_git_repo
    assert git_repo.branch_exists(default_branch)
    assert git_repo.branch_exists('feature_branch')
    assert not git_repo.branch_exists('nonexistent_branch')


def test_invalid_repo_path():
    with pytest.raises(ValueError):
        GitRepo('/path/to/non/existent/repo')
