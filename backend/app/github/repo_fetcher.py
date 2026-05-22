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

            try:

                contents = repository.get_contents(
                    item.path
                )

                content = contents.decoded_content.decode(
                    "utf-8",
                    errors="ignore"
                )

                java_files.append({
                    "path": item.path,
                    "content": content
                })

            except Exception as e:

                print(
                    f"failed to fetch : {item.path} / {e}"
                )

    return java_files