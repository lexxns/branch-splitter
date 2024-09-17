def test_create_branch(branch_manager, mock_git_repo):
    mock_git_repo.create_branch.return_value = True
    assert branch_manager.create_branch("new_branch")
    assert "new_branch" in branch_manager.get_branches()
    mock_git_repo.create_branch.assert_called_once_with("new_branch")


def test_create_branch_failure(branch_manager, mock_git_repo):
    mock_git_repo.create_branch.return_value = False
    assert not branch_manager.create_branch("failed_branch")
    assert "failed_branch" not in branch_manager.get_branches()


def test_get_branches(branch_manager):
    branch_manager.branches = ["branch1", "branch2"]
    assert branch_manager.get_branches() == ["branch1", "branch2"]


def test_push_branches(branch_manager, mock_git_repo):
    branch_manager.branches = ["branch1", "branch2"]
    mock_git_repo.push_branch.side_effect = [True, False]
    result = branch_manager.push_branches()
    assert result == {"branch1": True, "branch2": False}
    mock_git_repo.push_branch.assert_any_call("branch1")
    mock_git_repo.push_branch.assert_any_call("branch2")


def test_apply_change_to_branches(branch_manager, mock_git_repo):
    branch_manager.branches = ["branch1", "branch2"]
    mock_git_repo.apply_change.side_effect = [True, False]
    change = {"some": "change"}
    result = branch_manager.apply_change_to_branches(change, ["branch1", "branch2", "branch3"])
    assert result == {"branch1": True, "branch2": False, "branch3": False}
    mock_git_repo.apply_change.assert_any_call(change, "branch1")
    mock_git_repo.apply_change.assert_any_call(change, "branch2")


def test_remove_branch(branch_manager):
    branch_manager.branches = ["branch1", "branch2"]
    assert branch_manager.remove_branch("branch1")
    assert branch_manager.get_branches() == ["branch2"]
    assert not branch_manager.remove_branch("nonexistent_branch")
