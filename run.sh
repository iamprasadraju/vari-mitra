export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/opt/zbar/lib:${DYLD_FALLBACK_LIBRARY_PATH:-}"
uv run python3 manage.py runserver
