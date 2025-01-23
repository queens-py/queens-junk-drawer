import argparse
from preview_html_from_pr import preview_html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get HTML from PR artifact for preview."
    )
    parser.add_argument("pr", type=int, help="The ID of the pull request.")
    parser.add_argument("token", type=str, help="Github token.")
    args = parser.parse_args()

    REPO = "queens-py/queens"
    WORKFLOW_NAME = "tests_local"
    ARTIFACT_NAME = "html-coverage-report"
    preview_html(args.pr, args.token, REPO, WORKFLOW_NAME, ARTIFACT_NAME)
