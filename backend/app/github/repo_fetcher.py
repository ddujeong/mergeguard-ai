import os

from github import Github


github_client = Github(
    os.getenv("GITHUB_TOKEN")
)


def fetch_repo_tree(owner: str, repo: str):

    repository = github_client.get_repo(
        f"{owner}/{repo}"
    )

    tree = repository.get_git_tree(
        repository.default_branch,
        recursive=True
    )

    java_files = []

    for item in tree.tree:

        if item.path.endswith(".java"):
            java_files.append(item.path)

    return java_files