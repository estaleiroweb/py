# Build PyPi Package by GitHub

## Create the repository in GitHub
- Create an account in [github](https://github.com/) if not exists
- Create an repository there

## Create Token in Pypi
- Go to in Config Account
- Scroll down until API Tokens
- Click in Add API token
- Choice name and select All Account
- Click in Add token
- Click in copy Token

## Match GitHub with PyPi
- With the token (last topic) copied, go to GitHub repository
- Click in Settings
- Click in Secrets - Actions
- Click in New repository secret
- Put in name: PYPI_PASSWORD
- Put in Secret: `<the token copied>`
- Click again in New repository secret
- Put in name: PYPI_USERNAME
- Put in Secret: `<your pypi username>`

## Create git files in you package
In root of the package, create:
- .gitignore
  ```
	.vscode
	venv
	htmlcov
	dist
	.coverage
	__pycache__
	*.egg-info
	*.tar.gz
	.mypy_cache
  ```
- Like [setup.md](setup.md): setup.py, LICENCE, requirements.txt


## Link GitHub to PyPi
- In you repository, go to settings-Secrets.
- In Action secrets define the passwords geting them in PyPi Token

## Push all files to GitHub
```bash
git add .
git commint -m 'your comment'
git push
```

## Create a new realese in GitHub
The release must be have a format like 0.1.1

## Links
- [https://www.youtube.com/watch?v=r-wwMk5faXo](https://www.youtube.com/watch?v=r-wwMk5faXo)
- [https://www.youtube.com/watch?v=U-aIPTS580s](https://www.youtube.com/watch?v=U-aIPTS580s)
- [https://www.youtube.com/watch?v=0CeYPSffhLI](https://www.youtube.com/watch?v=0CeYPSffhLI)