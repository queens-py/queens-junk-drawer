import argparse
import os
import tarfile
import tempfile
import time
import webbrowser
import zipfile
from pathlib import Path

import requests
from github import Auth, Github


REPO = "queens-py/queens"
WORKFLOW_NAME = "build_documentation"
ARTIFACT_NAME = "github-pages"


def wait_for_keyboard_interrupt():
    print("Press Ctrl+C to delete the html preview")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def get_artifact(PR_number, zip_path, token):
    def download_artifact(url, file_name, **kwargs):
        print(f"\nDownloading artifact to {file_name}")
        response = requests.get(url, timeout=5, **kwargs)

        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
            print("Artifact downloaded successfully.")
        else:
            raise ValueError(f"Failed to download artifact: {response.status_code}")

    auth = Auth.Token(token)
    gh = Github(auth=auth)

    repo = gh.get_repo(REPO)

    pull_request = repo.get_pull(PR_number)

    print("\n")
    print(pull_request)
    print("\n")
    workflow_runs = repo.get_workflow_runs(branch=pull_request.head.ref)
    sorted_workflows = sorted(workflow_runs, key=lambda a: a.created_at, reverse=True)

    done = False
    for run in sorted_workflows:
        if (
            run.name != WORKFLOW_NAME
            or run.status != "completed"
            or run.conclusion != "success"
        ):
            continue

        artifacts = run.get_artifacts()
        sorted_artifacts = sorted(artifacts, key=lambda a: a.created_at)

        for artifact in sorted_artifacts:
            if artifact.name == ARTIFACT_NAME:
                print(
                    f"Using Workflow: {run.name}\n Run ID: {run.id}\n Status: {run.status}\n Conclusion: {run.conclusion}\n Date {run.created_at}"
                )
                print("\n")
                print(
                    f"Using Artifact: {artifact.name}\n ID: {artifact.id}\n Created At: {artifact.created_at}\n Download URL: {artifact.archive_download_url}\n"
                )
                download_artifact(
                    artifact.archive_download_url,
                    zip_path,
                    headers={"Authorization": f"token {token}"},
                )
                done = True
                break
        if done:
            break


def extract_html(zip_path, tmp_dir):

    print("Extracting the zip.")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(tmp_dir)

    print("Extracting the tar.")
    with tarfile.open(zip_path.with_suffix(".tar"), "r") as tar:
        tar.extractall(tmp_dir)


def preview_html(PR_number, token):
    with tempfile.TemporaryDirectory() as tmp_dir:

        tmp_dir = Path(tmp_dir)
        os.chdir(str(tmp_dir.resolve()))
        print("-" * 80)
        print(f"Using dir {tmp_dir.resolve()}")
        print("-" * 80)

        zip_path = tmp_dir / "artifact.zip"

        print("-" * 80)
        print("Getting the artifact.")
        get_artifact(PR_number, zip_path, token)
        print("-" * 80)

        print("-" * 80)
        print("Extracting the documentation.")
        extract_html(zip_path, tmp_dir)
        print("-" * 80)

        print("-" * 80)
        webbrowser.open("file://" + str(tmp_dir / "index.html"))
        wait_for_keyboard_interrupt()
        print("-" * 80)

        print("Deleting files")

        print("Bye bye.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get HTML documentation for preview.")
    parser.add_argument("pr", type=int, help="The ID of the pull request.")
    parser.add_argument("token", type=str, help="Github token.")
    args = parser.parse_args()

    preview_html(args.pr, args.token)
