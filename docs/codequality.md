## Code Quality
1. This project uses [ruff code formatter](https://docs.astral.sh/ruff/formatter/) to achieve consistency in formatting code in line with [PEP 8](https://peps.python.org/pep-0008/) standards
2. Whenever changes are made to code, run `ruff format` to format the changed files
3. Ruff also enforces `PEP8` standards and detects non conformant code through linting
4. Whenever changes are made to code, run `ruff check` to check for non comformant code
To easily enforce these standards, you can do the following 
* Go the `.git/hooks` folder and add create a `pre-commit` file then add the following
```bash 
#!/bin/sh

# Get the list of staged Python files
files=$(git diff --name-only --cached --diff-filter=d -- '*.py')

# If there are any Python files staged, format them with Ruff
if [ -n "$files" ]; then
    echo "Running ruff formatter on staged files..."
    ruff format $files

    # Add the formatted files back to staging
    git add $files
    echo "Running ruff linting tool on staged files..."
    ruff check $files --fix
    # Add fixed & linted files back to staging
    git add $files
else
   echo "No staged files found to run ruff formatter on ..."
fi
```
This custom precommit hook will ensure that all changed files are linted and formatted when `git commit` is run
* Ensure you run `chmod +x .git/pre-commit` to make the script exec