# Preview documentation locally

Install all the packages and run:
```bash
python <script_directory>/preview_documentation.py <pull_request_number> <your_github_token>
```

You need a GitHub token. Create one for "queens-py/queens" with read permission for metadata, pull requests and actions, read only is enough. Do not push your token to GitHub. Once you exit the Python program, the html files will be deleted.

# Add to your bashrc

Add alias in the bashrc file to make your life easy.

For the documentation
```bash
preview_documentation_queens_pr(){
    <python_directory>/python <script_directory>/preview_documentation.py $1 <your_github_token> ;
}
```
For the coverage report
```bash
preview_coverage_queens_pr(){
    <python_directory>/python <script_directory>/preview_coverage.py $1 <your_github_token> ;
}
```
