import re


def parse_diff_text(diff_text: str):

    files = []

    split_files = diff_text.split("diff --git")

    for chunk in split_files:

        if not chunk.strip():
            continue

        lines = chunk.strip().splitlines()

        filename = "unknown"

        additions = 0

        deletions = 0

        patch_lines = []

        for line in lines:

            if line.startswith("+++ b/"):

                filename = line.replace("+++ b/", "")

            if line.startswith("+") and not line.startswith("+++"):
                additions += 1

            if line.startswith("-") and not line.startswith("---"):
                deletions += 1

            patch_lines.append(line)

        files.append({
            "filename": filename,
            "additions": additions,
            "deletions": deletions,
            "patch": "\n".join(patch_lines)
        })

    return files