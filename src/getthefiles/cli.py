# src/github_folder_downloader/cli.py
import typer
from typing_extensions import Annotated 
# from .core import folderDownload


app = typer.Typer(help="A fast, non-cloning CLI tool to download specific GitHub sub-directories.")

@app.command()
def main_cli(
    repo: Annotated[str, typer.Argument(help="Include your target repo's name")],
    output: Annotated[str, typer.Option("--output", "-o", help="Directory to donwload in"), show_default='cwd'] = None,
    token: Annotated[str,typer.Option("--token", "-t", help="GitHub Personal Access Token for higher rate limits (optional).")] = None):
    pass
 
if __name__ == "__main__":
    app()
