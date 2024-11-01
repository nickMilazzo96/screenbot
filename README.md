Hermit: https://cashapp.github.io/hermit/usage/get-started/

UV: https://docs.astral.sh/uv/

Just: https://just.systems/man/en/

#

Installed Hermit following instructions
curl -fsSL https://github.com/cashapp/hermit/releases/download/stable/install.sh | /bin/bash

Added /Users/fwallace/bin to PATH in zshrc so Hermit is in PATH
Ran hermit init
Added shell hooks according to: https://cashapp.github.io/hermit/usage/shell/

Installed uv and just (hermit install uv, hermit install just, hermit install ruff)
uv init
file ~/Library/Caches/hermit/binaries/uv-0.4.29/uv
Added packages (uv add ...)

Now you can run everything in a virtual environment:

```sh
screenbot🐚 fwallace/setup-dev-env [~/dev/screenbot] >uv run python main/screenbot_funcs.py
Traceback (most recent call last):
  File "/Users/fwallace/dev/screenbot/main/screenbot_funcs.py", line 94, in <module>
    pubmed_scrape()
TypeError: pubmed_scrape() missing 4 required positional arguments: 'ncbi_email', 'search_string', 'max_results', and 'min_date'
```

TODO:

Add just commands for:

- lint
- format
- type check

- format on save in VS code
- Install Ruff extension in VS Code

```js
"[python]": {
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"
  }
}
```

Next:

- Add CI on GH actions
- Setup simple server
