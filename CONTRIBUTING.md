# Contribution Guidelines
First off, thanks for looking at our little game repo. There are a handful of guidelines here. If you have more suggestions, please make a PR following the existing guidelines.
## Style
### Git
* All commits should be [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). Extended options such as `refactor`, `docs`, and `chore` are welcome.
* Commit messages should be written in the present imperative, so `docs: add CONTRIBUTING.md` not `docs: added CONTRIBUTING.md`.
### Code
* All code is written in Python 3.10+. We recommend using the PyCharm IDE for formatting recommendations and ease of use.
* Code should be linted.
* Code should contain docstrings for any new classes or complex functions.
### Versioning
If you are making a breaking change, feature update, or bugfix, be sure to update [version.txt](https://github.com/thepolytheist/goblin-commander/blob/main/version.txt) appropriately. Version bumps will not be expected for other commits or PRs.