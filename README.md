# Screenbot

TODO(nmilazzo): Description of the repo

## Developing

### IDE

We recommend using Visual Studio Code and installing the following extensions:

- vscode-just
- ruff
- Python

We also recommend adding the following to your `settings.json`:

```json
// Python settings
"python.analysis.autoImportCompletions": true,
"[python]": {
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"
  }
}
```

### Tooling

This project uses the following tools for environment management:

- [Hermit](https://cashapp.github.io/hermit/usage/get-started/) manages the installed tools
- [uv](https://docs.astral.sh/uv/) manages Python and our project environments
- [just](https://just.systems/man/en/) makes it extremely simple to run commands

To begin, follow instructions to install Hermit. You may also need to add the install path to your PATH. Replace the
path and filename in this command appropriately:

```sh
echo "export PATH=$PATH:/path/to/hermit/bin" >> ~/.zshrc
```

It's recommended to [add Hermit shell hooks](https://cashapp.github.io/hermit/usage/shell/) as well.

Now, you can simply run `just setup` to setup your virtual environment. Other commands are available to support
development - simply run `just` to see the full list.

You may also use `uv` to interact with the virtual environment. For example, to run any commands in your virtual
environment, run `uv run ...`, e.g. `uv run python screenbot.py`.
