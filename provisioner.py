import os
import base64
import logging

from github import Github, Auth, GithubException



def create_repo(org, repo_name, description, token):
    """
    Create a private GitHub repo under the given user account.

    Args:
        org: GitHub username
        repo_name: name of the repo to create
        description: repo description
        token: GitHub personal access token

    Returns:
        (success: bool, message: str)
    """
    try:
        g = Github(auth=Auth.Token(token))
        repo = g.get_user().create_repo(repo_name, description=description, private=True)
        repo.create_file("README.md", "Initial commit", "# " + repo_name) #create branch and readme

        message = f"Created repo '{repo_name}'"
        logging.info(message)
        return True, message
    except GithubException as e:
        message = f"Failed to create repo '{repo_name}': {e.data.get('message', str(e))}"
        logging.error(message)
        return False, message
    except Exception as e:
        message = f"Unexpected error creating repo '{repo_name}': {e}"
        logging.error(message)
        return False, message


def add_member(org, repo_name, github_username, member_role, token):
    """
    Add a GitHub user as a collaborator on a repo with permission matching their role.
    "admin" role gets "admin" permission, "developer" role gets "push" permission.

    Args:
        org: GitHub organization name
        repo_name: name of the repo
        github_username: GitHub username to add
        member_role: "admin" or "developer"
        token: GitHub personal access token

    Returns:
        (success: bool, message: str)
    """
    try:
        permission = "admin" if member_role == "admin" else "push"
        g = Github(auth=Auth.Token(token))
        repo = g.get_repo(f"{org}/{repo_name}")
        repo.add_to_collaborators(github_username, permission=permission)
        message = f"Added '{github_username}' to '{repo_name}' with '{permission}' permission"
        logging.info(message)
        return True, message
    except GithubException as e:
        message = f"Failed to add '{github_username}' to '{repo_name}': {e.data.get('message', str(e))}"
        logging.error(message)
        return False, message
    except Exception as e:
        message = f"Unexpected error adding '{github_username}' to '{repo_name}': {e}"
        logging.error(message)
        return False, message


def set_branch_protections(org, repo_name, token):
    """
    Protect the "main" branch of a repo: require 1 pull request review before
    merging, dismiss stale PR approvals, and require status checks (tests) to pass.

    Args:
        org: GitHub organization name
        repo_name: name of the repo
        token: GitHub personal access token

    Returns:
        (success: bool, message: str)
    """
    try:
        g = Github(auth=Auth.Token(token))
        repo = g.get_repo(f"{org}/{repo_name}")
        branch = repo.get_branch("main")
        branch.edit_protection(
            required_approving_review_count=1,
            dismiss_stale_reviews=True,
            strict=True,
            contexts=["test"],
        )
        message = f"Set branch protections on 'main' for '{repo_name}'"
        logging.info(message)
        return True, message
    except GithubException as e:
        message = f"Failed to set branch protections for '{repo_name}': {e.data.get('message', str(e))}"
        logging.error(message)
        return False, message
    except Exception as e:
        message = f"Unexpected error setting branch protections for '{repo_name}': {e}"
        logging.error(message)
        return False, message


def _record(repo_name, action, success, message, member=None):
    """Build a success/failure tracking dict for one provisioning action."""
    record = {"repo_name": repo_name, "action": action}
    if member is not None:
        record["member"] = member
    if success:
        record["details"] = message
    else:
        record["error"] = message
    return record


def provision_all_teams(valid_rows, token, org, templates_path):
    """
    Main orchestration function. For each validated CSV row: create the repo
    (once per repo_name), add the row's member, then protect and template the
    repo (each once per repo_name).

    Args:
        valid_rows: list of validated row dicts with keys repo_name, description,
            github_username, member_roles
        token: GitHub personal access token
        org: GitHub organization name
        templates_path: path to the folder containing run-test.yml

    Returns:
        (successes: list[dict], failures: list[dict])
    """
    repos_created = set()
    repos_protected = set()

    successes = []
    failures = []

    for row in valid_rows:
        repo_name = row["repo_name"]
        description = row.get("description", "")
        github_username = row["github_username"]
        member_role = row["member_roles"]

        if repo_name not in repos_created:
            success, message = create_repo(org, repo_name, description, token)
            record = _record(repo_name, "create_repo", success, message)
            (successes if success else failures).append(record)
            if success:
                repos_created.add(repo_name)

        success, message = add_member(org, repo_name, github_username, member_role, token)
        record = _record(repo_name, "add_member", success, message, member=github_username)
        (successes if success else failures).append(record)

        if repo_name not in repos_protected:
            success, message = set_branch_protections(org, repo_name, token)
            record = _record(repo_name, "set_branch_protections", success, message)
            (successes if success else failures).append(record)
            if success:
                repos_protected.add(repo_name) 

    return successes, failures
