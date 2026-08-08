# delete_repos.py

import os
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()

def delete_repos(repo_names, token, org):
    """
    Delete GitHub repos by name.
    
    Args:
        repo_names: list of repo names to delete
        token: GitHub personal access token
        org: GitHub username
    """

    if not token or not org:
        print("ERROR: GITHUB_TOKEN or GITHUB_ORG not in .env")
        return
    
    print(f"Deleting repos: {repo_names}")


    g = Github(auth=Auth.Token(token))
    user = g.get_user()
    
    for repo_name in repo_names:
        try:
            repo = user.get_repo(repo_name)
            repo.delete()
            print(f"✓ Deleted repo '{repo_name}'")
        except Exception as e:
            print(f"✗ Failed to delete '{repo_name}': {e}")

if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_ORG")
    
    # List of repos to delete
    repos_to_delete = ["ai-assistant", "data-pipeline", "frontend-ui"]
    
    delete_repos(repos_to_delete, token, username)