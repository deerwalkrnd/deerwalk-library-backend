# Deerwalk Library Project

1. Use this as your VSCode Users/settings.json

```json
{
  "security.workspace.trust.untrustedFiles": "open",
  "workbench.colorTheme": "Default Dark+",
  "editor.fontFamily": "FiraCode Nerd Font Mono, Fira Code, monospace",
  "editor.fontWeight": "600",
  "editor.fontLigatures": true,
  "workbench.iconTheme": "material-icon-theme",
  "workbench.sideBar.location": "right",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.pylintArgs": [
    "--load-plugins=pylint_mypy",
    "--enable=invalid-name,missing-function-docstring"
  ],
  "python.formatting.provider": "ruff",
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingTypeStubs": "warning",
    "reportUntypedFunctionDecorator": "warning"
  },
  "editor.inlayHints.enabled": "on",
  "python.analysis.inlayHints.functionReturnTypes": true,
  "python.analysis.inlayHints.variableTypes": true
}

```

2. Run the run.sh command to run the application.


### Conventions followed
- Class and method docstring: [Google docstring](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)