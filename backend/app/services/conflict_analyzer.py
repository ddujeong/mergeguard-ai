from app.services.github_service import (
    parse_pr_url,
    get_open_pull_requests,
    get_pull_request_files,
)


def analyze_conflicts(pr_url: str, current_files: list):

    owner, repo, current_pr_number = parse_pr_url(pr_url)

    open_prs = get_open_pull_requests(owner, repo)

    current_filenames = {
        file["filename"]
        for file in current_files
    }

    conflict_prs = []

    for pr in open_prs:

        if str(pr["number"]) == current_pr_number:
            continue

        pr_files = get_pull_request_files(
            owner,
            repo,
            pr["number"]
        )

        other_filenames = {
            file["filename"]
            for file in pr_files
        }

        overlaps = list(
            current_filenames & other_filenames
        )

        if overlaps:

            conflict_prs.append({
                "pr_number": pr["number"],
                "title": pr["title"],
                "overlapping_files": overlaps
            })

    return {
        "conflict_count": len(conflict_prs),
        "conflict_prs": conflict_prs
    }