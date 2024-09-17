import typer
from typing import List

from branch_splitter.change_manager import Change


class UserInterface:
    def __init__(self):
        self.typer = typer.Typer()

    def prompt_for_branches(self) -> List[str]:
        # Prompt user to input new branch names
        # Use typer.prompt() for input
        branches = []
        while True:
            branch = typer.prompt("Enter a new branch name (or press Enter to finish)")
            if not branch:
                break
            branches.append(branch)
        return branches

    def prompt_for_change_assignment(self, change: Change, branches: List[str]) -> List[str]:
        # Display change and prompt user to assign to branches
        # Use typer.echo() for output and typer.prompt() for input
        typer.echo(f"Change: {change.message}")
        typer.echo(f"Diff: {change.diff}")
        selected = typer.prompt(
            "Select branches to apply this change (comma-separated numbers)",
            default="",
        )
        selected_indices = [int(i.strip()) for i in selected.split(",") if i.strip()]
        return [branches[i] for i in selected_indices if i < len(branches)]

    def confirm_push(self, branch: str, changes: List[Change]) -> bool:
        # Display summary and confirm push for a branch
        typer.echo(f"Branch: {branch}")
        for change in changes:
            typer.echo(f"- {change.message}")
        return typer.confirm(f"Push branch '{branch}'?")

    def display_summary(self, branches: List[str], changes: List[Change]):
        # Display final summary of all branches and their changes
        for branch in branches:
            typer.echo(f"Branch: {branch}")
            for change in changes:
                typer.echo(f"- {change.message}")
            typer.echo("---")
