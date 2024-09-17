import typer
from typing import List
from branch_splitter.git_repo import GitRepo
from branch_splitter.branch_manager import BranchManager


class UserInterface:
    def __init__(self, git_repo: GitRepo, branch_manager: BranchManager):
        self.git_repo = git_repo
        self.branch_manager = branch_manager
        self.app = typer.Typer()
        self.setup_commands()

    def setup_commands(self):
        @self.app.command()
        def create_branches(names: List[str] = typer.Argument(..., help="Names of branches to create")):
            """Create new branches."""
            for name in names:
                if self.branch_manager.create_branch(name):
                    typer.echo(f"Created branch: {name}")
                else:
                    typer.echo(f"Failed to create branch: {name}")

        @self.app.command()
        def list_branches():
            """List all managed branches."""
            branches = self.branch_manager.get_branches()
            if branches:
                typer.echo("Managed branches:")
                for branch in branches:
                    typer.echo(f"- {branch}")
            else:
                typer.echo("No branches are currently managed.")

        @self.app.command()
        def push_branches():
            """Push all managed branches."""
            results = self.branch_manager.push_branches()
            for branch, success in results.items():
                if success:
                    typer.echo(f"Successfully pushed branch: {branch}")
                else:
                    typer.echo(f"Failed to push branch: {branch}")

        @self.app.command()
        def apply_changes(source_branch: str = typer.Option(..., help="Source branch with changes"),
                          target_branch: str = typer.Option(..., help="Target branch to compare against")):
            """Apply changes from source branch to target branches."""
            changes = self.git_repo.get_changes(source_branch, target_branch)
            if not changes:
                typer.echo("No changes found.")
                return

            for i, change in enumerate(changes):
                typer.echo(f"\nChange {i + 1}:")
                typer.echo(f"File: {change['file']}")
                typer.echo(f"Commit: {change['commit_hash']}")
                typer.echo(f"Message: {change['message']}")
                typer.echo("Diff:")
                typer.echo(change['diff'])

                apply_to = typer.prompt(
                    "Apply this change to which branches? (comma-separated list, or 'all' for all managed branches)")
                if apply_to.lower() == 'all':
                    target_branches = self.branch_manager.get_branches()
                else:
                    target_branches = [b.strip() for b in apply_to.split(',')]

                results = self.branch_manager.apply_change_to_branches(change, target_branches)
                for branch, success in results.items():
                    if success:
                        typer.echo(f"Successfully applied change to branch: {branch}")
                    else:
                        typer.echo(f"Failed to apply change to branch: {branch}")

    def run(self):
        self.app()
