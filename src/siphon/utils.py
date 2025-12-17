# src/siphon/utils.py

import requests
import os
from typing import Optional, Dict



def configure_session(token: Optional[str]) -> requests.Session:
   s = requests.Session()
   s.headers.update({
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    })
   if token:
        s.headers.update({"Authorization": f"Bearer {token}"})
   return s


def create_local_dirs(filepath: str) -> None:
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    return

def determine_local_root(repo: str, path: str, output: Optional[str]) -> str:
    """
    Calculates the final local root directory path for saving files.
    """
    if output:
        local_root = output
    else:
        local_root = path.rstrip('/').split('/')[-1]
        if not local_root: 
            local_root = repo.rsplit('/')[-1] # download whole repo

    create_local_dirs(local_root)
    return local_root