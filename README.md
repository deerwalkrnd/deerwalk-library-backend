# Deerwalk Library Project

1. Use this as your VSCode Users/settings.json

```json

{
  "security.workspace.trust.untrustedFiles": "open",
  "workbench.colorTheme": "Houston",
  "editor.fontFamily": "FiraCode Nerd Font Mono, Fira Code, monospace",
  "editor.fontWeight": "600",
  "editor.fontLigatures": true,
  "workbench.iconTheme": "material-icon-theme",
  "workbench.sideBar.location": "right",
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.autoImportCompletions": true,
  "editor.inlayHints.enabled": "on",
  "python.analysis.inlayHints.functionReturnTypes": true,
  "python.analysis.inlayHints.variableTypes": true,
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "ruff.interpreter": ["./.venv/bin/python"],
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}

```

2. Run the run.sh command to run the application.


### Conventions followed
- Class and method docstring: [Google docstring](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)

## Aashutosh Tasks
1. Seeder Implementation - DONE
2. Auth Implementation ( Librarian and <7 ) - DONE
3. User CRUD - DOING
4. Celery Implementation
