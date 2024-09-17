from unittest.mock import patch, Mock

from typer.testing import CliRunner

from branch_splitter.main import app as _app


def test_main_controller_initialization(controller, mock_git_repo, mock_branch_manager, mock_user_interface):
    assert isinstance(controller.git_repo, Mock)
    assert isinstance(controller.branch_manager, Mock)
    assert isinstance(controller.user_interface, Mock)


def test_main_controller_run(controller, mock_git_repo, mock_user_interface):
    mock_git_repo.return_value.get_current_branch.return_value = "main"
    mock_git_repo.return_value.repo.working_dir = "/mock/repo/path"

    with patch('main_controller.typer.prompt') as mock_prompt:
        mock_prompt.side_effect = ["1", "new_branch", "5"]
        controller.run()

    mock_user_interface.return_value.app.assert_called_once_with(["create-branches", "new_branch"])


def test_main_function(mock_git_repo, mock_branch_manager, mock_user_interface):
    runner = CliRunner()
    with patch('main_controller.typer.prompt') as mock_prompt:
        mock_prompt.side_effect = ["/mock/repo/path", "5"]
        result = runner.invoke(_app)

    assert result.exit_code == 0
    assert "Welcome to the Git Branch Splitter!" in result.output
    assert "Exiting the program. Goodbye!" in result.output


def test_invalid_action(controller, mock_git_repo):
    mock_git_repo.return_value.get_current_branch.return_value = "main"
    mock_git_repo.return_value.repo.working_dir = "/mock/repo/path"

    with patch('branch_splitter.main_controller.typer.prompt') as mock_prompt, \
            patch('branch_splitter.main_controller.typer.echo') as mock_echo:
        mock_prompt.side_effect = ["invalid", "5"]
        controller.run()

    mock_echo.assert_any_call("Invalid choice. Please try again.")
