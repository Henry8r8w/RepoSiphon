# src/github_folder_downloader/cli.py
import typer
from typing_extensions import Annotated

from getthefiles.core import download_folder 



app = typer.Typer(help="A fast, non-cloning CLI tool to download specific GitHub sub-directories.")

@app.command()
def main_cli(
    repo: Annotated[str, typer.Argument(help="Include your target repo's name")],
    path: Annotated[str, typer.Argument(help="The sub-directory path within the repository (e.g., 'scripts').")],
    output: Annotated[str, typer.Option("--output", "-o", help="Directory to donwload in", show_default='cwd')] = None,
    token: Annotated[str,typer.Option("--token", "-t", help="GitHub Personal Access Token for higher rate limits (optional).")] = None):
    
    try:
        download_folder(repo, path, output, token)
        typer.echo("\n Operation complete!")
    except typer.Exit as e:
        raise e
    except Exception as e:
        typer.echo(f"\n A critical error occurred: {e}", err=True)
        raise typer.Exit(code=1)
 
if __name__ == "__main__":
    app()


