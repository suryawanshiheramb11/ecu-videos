import os
import uuid
from github import Github
from dotenv import load_dotenv

load_dotenv()

def upload_video(file_path, repo_name, token=None):
    """
    Uploads a video file to a GitHub repository and returns the raw URL.
    
    Args:
        file_path (str): Path to the local video file.
        repo_name (str): Name of the GitHub repository (e.g., 'username/repo').
        token (str): GitHub Personal Access Token. If None, loads from env.
        
    Returns:
        str: The raw URL of the uploaded video.
    """
    if not token:
        token = os.getenv("GITHUB_TOKEN")
        
    if not token:
        raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in .env or pass it explicitly.")

    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Generate a unique filename to prevent collisions
    unique_filename = f"{uuid.uuid4()}.mp4"
    
    # Read the video file
    with open(file_path, "rb") as f:
        content = f.read()
        
    # Upload to GitHub
    # Note: GitHub API has a limit of 100MB for files via API. 
    # Videos should be small enough for this use case.
    repo.create_file(
        path=unique_filename,
        message=f"Add video {unique_filename}",
        content=content,
        branch="main" 
    )
    
    # Construct the raw URL
    # Assuming 'main' branch. 
    # For private repos, this URL might not work directly in <img> or <video> tags without auth.
    # But for public repos, it works perfectly.
    raw_url = f"https://raw.githubusercontent.com/{repo_name}/main/{unique_filename}"
    
    return raw_url
