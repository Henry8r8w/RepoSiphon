# src/siphon/core.py

import requests
import os
import typer
from typing import Optional, List, Tuple

from .utils import configure_session, determine_local_root
from .threading_manager import ThreadingManager

GITHUB_API_URL = "https://api.github.com" 
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


def traverse_api_tree(repo: str,  api_path: str, local_root: str, session: requests.Session) -> List[DownloadJob]:
    """
    Recursively fetches content from the GitHub Content API
    """
    url = f"https://api.github.com/repos/{repo}/contents/{api_path}"
    response = session.get(url)
    if response.status_code != 200:
        print(f"Error accessing {url}: {response.status_code}")
        return []

    data = response.json()
    jobs: List[DownloadJob] = []
    
    # Single File Case
    if isinstance(data, dict):
        if data['type'] == 'file':
            save_path = os.path.join(local_root, data['name'])
            jobs.append((data['download_url'], save_path))
        return jobs
    
    # Standard Case
    for item in data:
        name = item['name']
        item_local_path = os.path.join(local_root, name)
        if item['type'] == 'file':
            if item.get('download_url'):
                jobs.append((item['download_url'], item_local_path))
        elif item['type'] == 'dir':
            sub_jobs = traverse_api_tree(
                repo=repo,
                api_path=item['path'],       
                local_root=item_local_path, 
                session=session
            )
            jobs.extend(sub_jobs)

    return jobs

def download_folder(repo: str, path: str, output: Optional[str] = None, token: Optional[str] = None) -> None:
    """
    Call all cores and compose the program alltogether. 
    """
    session = configure_session(token)
    local_root = determine_local_root(repo, path, output) 
    typer.echo(f"\n Compiling file list for {repo}/{path}...")
    download_jobs = traverse_api_tree(repo, path, local_root, session)
    if not download_jobs:
        typer.echo("No files found to download.")
        return
    typer.echo(f"\n Found {len(download_jobs)} files. Starting parallel download to '{local_root}'...")
    manager = ThreadingManager(download_jobs, session)
    manager.execute_downloads()