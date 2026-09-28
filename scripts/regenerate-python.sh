#!/usr/bin/env bash
# Regenerates python/src/status200uploads/_generated from openapi/openapi.yaml.
#
#   pip install -r python/tools/requirements.txt
#   bash scripts/regenerate-python.sh
#
# The generated files are never edited by hand: change openapi/openapi.yaml (a copy of
# https://status200uploads.com/openapi.yaml) or python/openapi-python-client.yaml, then run this.
# CI runs it and fails when the result differs from what is committed.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_dir="$root/python"

want_generator="$(sed -n 's/^openapi-python-client==//p' "$python_dir/tools/requirements.txt")"
want_ruff="$(sed -n 's/^ruff==//p' "$python_dir/tools/requirements.txt")"
have_generator="$(openapi-python-client --version | awk '{print $NF}')"
have_ruff="$(ruff --version | awk '{print $NF}')"
if [ "$have_generator" != "$want_generator" ] || [ "$have_ruff" != "$want_ruff" ]; then
  echo "Need openapi-python-client $want_generator and ruff $want_ruff (found $have_generator and $have_ruff):" >&2
  echo "  pip install -r python/tools/requirements.txt" >&2
  exit 1
fi

cd "$python_dir"
python tools/v2_only.py "$root/openapi/openapi.yaml" build/openapi-v2.json
openapi-python-client generate \
  --path build/openapi-v2.json \
  --config openapi-python-client.yaml \
  --meta none \
  --output-path src/status200uploads/_generated \
  --overwrite
echo "Wrote python/src/status200uploads/_generated"
