# src/siphon/threading_manager.py

import concurrent.futures
from typing import List, Tuple, Optional
import typer
import requests

DownloadJob = Tuple[str, str] 

class ThreadingManager:
    MAX_WORKERS = 8 
    def __init__(self, download_jobs: List[DownloadJob], session: requests.Session):
        self.jobs = download_jobs
        self.session = session
        
    def execute_downloads(self) -> None:
        """Submits all download jobs to a ThreadPoolExecutor."""
        from .core import fetch_and_save 
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            future_to_job = {executor.submit(fetch_and_save, url, path, self.session): (url, path) 
                for url, path in self.jobs}
            
            for future in concurrent.futures.as_completed(future_to_job):
                url, path = future_to_job[future]
                try:
                    success = future.result() 
                    if success:
                        typer.echo(f"  [DONE] {path}", color=typer.colors.GREEN)
                    else:
                        typer.echo(f"  [FAIL] Failed to download {path}", color=typer.colors.RED, err=True)
                except Exception as exc:
                    typer.echo(f"  [ERROR] {path} generated an exception: {exc}", color=typer.colors.RED, err=True)