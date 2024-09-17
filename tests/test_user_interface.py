def test_create_branches(user_interface, runner, mock_branch_manager):
    mock_branch_manager.create_branch.side_effect = [True, False]
    result = runner.invoke(user_interface.app, ["create-branches", "branch1", "branch2"])
    assert result.exit_code == 0
    assert "Created branch: branch1" in result.stdout
    assert "Failed to create branch: branch2" in result.stdout


def test_list_branches(user_interface, runner, mock_branch_manager):
    mock_branch_manager.get_branches.return_value = ["branch1", "branch2"]
    result = runner.invoke(user_interface.app, ["list-branches"])
    assert result.exit_code == 0
    assert "branch1" in result.stdout
    assert "branch2" in result.stdout


def test_push_branches(user_interface, runner, mock_branch_manager):
    mock_branch_manager.push_branches.return_value = {"branch1": True, "branch2": False}
    result = runner.invoke(user_interface.app, ["push-branches"])
    assert result.exit_code == 0
    assert "Successfully pushed branch: branch1" in result.stdout
    assert "Failed to push branch: branch2" in result.stdout


def test_apply_changes(user_interface, runner, mock_git_repo, mock_branch_manager):
    mock_git_repo.get_changes.return_value = [
        {
            "file": "test.txt",
            "commit_hash": "abc123",
            "message": "Test commit",
            "diff": "Test diff"
        }
    ]
    mock_branch_manager.get_branches.return_value = ["branch1", "branch2"]
    mock_branch_manager.apply_change_to_branches.return_value = {"branch1": True, "branch2": False}

    result = runner.invoke(user_interface.app,
                           ["apply-changes", "--source-branch", "source", "--target-branch", "target"], input="all\n")

    assert result.exit_code == 0
    assert "Successfully applied change to branch: branch1" in result.stdout
    assert "Failed to apply change to branch: branch2" in result.stdout
