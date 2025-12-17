# RepoSiphon

**A high-performance, concurrent CLI tool for surgically downloading subdirectories from GitHub repositories.**

## ⚡ The Problem
GitHub does not provide a native way to download a single folder. Users are forced to `git clone` entire repositories, wasting bandwidth and storage.

**RepoSiphon** treats the GitHub API as a file system, recursively reconstructing target directories in memory and utilizing a concurrent worker pool to stream files to disk.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Henry8r8w/RepoSiphon.git](https://github.com/Henry8r8w/RepoSiphon.git)
    cd RepoSiphon
    ```

2.  **Install in editable mode (Recommended):**
    This allows you to run the tool from anywhere while developing.
    ```bash
    pip install -e .
    ```

## 💻 Usage

Run the tool as a python module.

### Basic Download
Download a specific folder (e.g., `RateMyProf Scrape/selenium`) from a repository.

```bash
# Syntax: python -m src.siphon.cli <OWNER>/<REPO> <PATH>
python -m src.siphon.cli Henry8r8w/Notebooks "RateMyProf Scrape/selenium"

