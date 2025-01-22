# Preview documentation locally

Install all the packages and run:
```bash
python preview_html_documentation_from_pr/preview_html_documentation_from_pr.py <pull_request_number> <your_github_token>
```

You need a GitHub token. Create one for "queens-py/queens" with read permission for metadata, pull requests and artifacts, read only is enough. Do not push your token to GitHub. Once you exit the Python program, the html files will be deleted.