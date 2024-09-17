import typer

from branch_splitter.main_controller import MainController

app = typer.Typer()


@app.command()
def main(repo_path: str = typer.Argument(".", help="Path to the Git repository")):
    controller = MainController(repo_path)
    controller.run()


if __name__ == "__main__":
    app()
