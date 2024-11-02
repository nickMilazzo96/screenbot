
UV := "bin/uv"
JUST := "bin/just"

default:
    just --list

setup:
    @{{ UV }} sync --frozen
    echo "Run source .venv/bin/activate to drop into your virtual environment"

pyright:
    @{{ UV }} run pyright .

format:
    @{{ UV }} run ruff format .

check:
    @{{ UV }} run ruff check .