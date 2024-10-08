from unittest.mock import Mock, patch

import pytest
from git import Repo
from typer.testing import CliRunner

from branch_splitter.branch_manager import BranchManager
from branch_splitter.git_repo import GitRepo
from branch_splitter.main_controller import MainController
from branch_splitter.user_interface import UserInterface


@pytest.fixture
def temp_git_repo(tmp_path):
    """
    Create a temporary Git repository for testing.
    """
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    repo = Repo.init(repo_path)

    # Create an initial commit
    file_path = repo_path / "initial_file.txt"
    file_path.write_text("Initial content")
    repo.index.add(["initial_file.txt"])
    repo.index.commit("Initial commit")

    # Determine the name of the default branch
    default_branch = repo.active_branch.name

    # Create a new branch
    repo.git.checkout('-b', 'feature_branch')

    # Make a change in the feature branch
    file_path.write_text("Feature branch content")
    repo.index.add(["initial_file.txt"])
    repo.index.commit("Feature branch commit")

    # Switch back to the default branch
    repo.git.checkout(default_branch)

    return repo_path, default_branch


@pytest.fixture
def git_repo(temp_git_repo):
    """
    Create a GitRepo instance for testing.
    """
    repo_path, _ = temp_git_repo
    return GitRepo(repo_path)


@pytest.fixture
def mock_git_repo():
    with patch('branch_splitter.main_controller.GitRepo') as mock:
        mock.return_value = mock
        mock.repo = Mock()
        mock.repo.working_dir = "/mock/repo/path"
        mock.get_current_branch.return_value = "main"
        yield mock


@pytest.fixture
def branch_manager(mock_git_repo):
    return BranchManager(mock_git_repo)


@pytest.fixture
def mock_branch_manager():
    with patch('branch_splitter.main_controller.BranchManager') as mock:
        yield mock


@pytest.fixture
def user_interface(mock_git_repo, mock_branch_manager):
    ui = UserInterface(mock_git_repo, mock_branch_manager)
    return ui


@pytest.fixture
def mock_user_interface():
    with patch('branch_splitter.main_controller.UserInterface') as mock:
        yield mock


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def controller(mock_git_repo, mock_branch_manager, mock_user_interface):
    return MainController("/mock/repo/path")
