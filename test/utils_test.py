# tests/utils_test.py
import pytest
from src.siphon.utils import configure_session, determine_local_root

# --- Test Session Configuration --- #
def test_configure_session_auth():
    # Token exist
    token = "ghp_SECRET123"
    session = configure_session(token)
    assert session.headers["Authorization"] == f"Bearer {token}"
    assert session.headers["Accept"] == "application/vnd.github+json"
    assert session.headers["X-GitHub-Api-Version"] == "2022-11-28"

def test_configure_session_no_auth():
    # Token does not exist
    session = configure_session(None)
    assert "Authorization" not in session.headers
    assert session.headers["Accept"] == "application/vnd.github+json"


# --- Test Local Root Determination --- #
def test_determine_local_root_logic(mocker):
    # Mock so we don't touch disk
    mocker.patch("src.siphon.utils.create_local_dirs")

    # Case A: User explicitly provides output "-o my_libs"
    assert determine_local_root("user/repo", "src/utils", output="my_libs") == "my_libs"

    # Case B: Default behavior (Use folder name)
    assert determine_local_root("user/repo", "src/utils", output=None) == "utils"

    # Case C: Path has trailing slash "src/utils/"
    assert determine_local_root("user/repo", "src/utils/", output=None) == "utils"
    
    # Case D: Path has trailing slash -> download whole repo
    assert determine_local_root("Henry/MyRepo", "", output=None) == "MyRepo"


if __name__ == "__main__":
    test_configure_session_auth()
    test_configure_session_no_auth()
    test_determine_local_root_logic(mocker)