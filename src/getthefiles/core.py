# src/github_folder_downloader/core.py

import requests
import os
import typer
from typing import Optional, List, Tuple

from .utils import create_local_dir, spinup_session
from .threading_manager import ThreadingManager

GITHUB_API_URL = "https://api.github.com" # GET　repos/{owner}/{repo}/contents/{path}
DownloadJob = Tuple[str, str] # (download_url, local_filepath)

def fetch_and_save(download_url: str, saving_filepath: str, session: requests.Session) -> bool:
    """
    Read session's content and write into user-specified directory.
    """
    response = session.get(download_url, stream=True)
    if response.status_code == 200:
        with open(saving_filepath, 'wb') as f:
            for content in response.iter_content(): 
                f.write(content)
        return True
    else:
        return False

def determine_local_root(repo: str, path: str, output: Optional[str]) -> str:
    """
    Calculates the final local root directory path for saving files.
    """
    if output:
        local_root = output
    else:
        local_root = path.rsplit('/').split('/')[-1]
    create_local_dir(local_root = local_root) 
    return local_root

def traverse_api_tree(repo: str, api_path: str,local_root: str,session: requests.Session) -> List[DownloadJob]:
    """
    Recursively fetches content from the GitHub Content API
    """
    pass

def download_folder(repo: str, path: str, output: Optional[str] = None, token: Optional[str] = None) -> None:
    """
    Call all cores and compose the program alltogether. 
    """
    session = spinup_session(token)
    local_root = determine_local_root(repo, path, output) 
    typer.echo(f"\n Compiling file list for {repo}/{path}...")
    download_jobs = traverse_api_tree(repo, path, local_root, session)
    if not download_jobs:
        typer.echo("No files found to download.")
        return
    typer.echo(f"\n Found {len(download_jobs)} files. Starting parallel download to '{local_root}'...")
    manager = ThreadingManager(download_jobs, session)
    manager.execute_downloads()