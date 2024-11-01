Hermit: https://cashapp.github.io/hermit/usage/get-started/

UV: https://docs.astral.sh/uv/

Just: https://just.systems/man/en/

#

Installed Hermit following instructions
curl -fsSL https://github.com/cashapp/hermit/releases/download/stable/install.sh | /bin/bash

Added /Users/fwallace/bin to PATH in zshrc so Hermit is in PATH
Ran hermit init
Added shell hooks according to: https://cashapp.github.io/hermit/usage/shell/

Installed uv and just (hermit install uv, hermit install just)
uv init
file ~/Library/Caches/hermit/binaries/uv-0.4.29/uv
Added packages (uv add ...)
