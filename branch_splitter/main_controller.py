import typer
from branch_splitter.git_repo import GitRepo
from branch_splitter.branch_manager import BranchManager
from branch_splitter.user_interface import UserInterface


class MainController:
    def __init__(self, repo_path: str):
        self.git_repo = GitRepo(repo_path)
        self.branch_manager = BranchManager(self.git_repo)
        self.user_interface = UserInterface(self.git_repo, self.branch_manager)

    def run(self):
        typer.echo(f"Found Git repository at: {self.git_repo.repo.working_dir}")
        typer.echo(f"Current branch: {self.git_repo.get_current_branch()}")

        while True:
            action = typer.prompt(
                "Choose an action:\n"
                "1. Create new branches\n"
                "2. List managed branches\n"
                "3. Push branches\n"
                "4. Apply changes\n"
                "5. Exit\n"
                "Enter the number of your choice"
            )

            if action == "1":
                branch_names = typer.prompt("Enter branch names (comma-separated)").split(",")
                self.user_interface.app(["create-branches"] + branch_names)
            elif action == "2":
                self.user_interface.app(["list-branches"])
            elif action == "3":
                self.user_interface.app(["push-branches"])
            elif action == "4":
                source_branch = typer.prompt("Enter source branch name")
                target_branch = typer.prompt("Enter target branch name")
                self.user_interface.app(
                    ["apply-changes", "--source-branch", source_branch, "--target-branch", target_branch])
            elif action == "5":
                typer.echo("Exiting the program. Goodbye!")
                break
            else:
                typer.echo("Invalid choice. Please try again.")


def main():
    typer.echo("Welcome to the Git Branch Splitter!")
    repo_path = typer.prompt("Enter the path to your Git repository")
    controller = MainController(repo_path)
    controller.run()


if __name__ == "__main__":
    typer.run(main)
