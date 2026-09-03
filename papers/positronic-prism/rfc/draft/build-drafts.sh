#!/usr/bin/env bash
# =====================================================================
# Build the PEEP ISE Internet-Drafts (RFCv3 markdown -> XML -> text)
#
# Requires: kramdown-rfc (ruby gem) + xml2rfc (pip). The script uses
# whatever xml2rfc is on PATH; if none, it tries the rfc-venv.
#
#   export PATH="$HOME/.local/share/gem/ruby/3.3.0/bin:$PATH"
#   ./build-drafts.sh
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v xml2rfc >/dev/null 2>&1; then
  if [ -x /tmp/opencode/rfc-venv/bin/xml2rfc ]; then
    export PATH="/tmp/opencode/rfc-venv/bin:$PATH"
  else
    echo "xml2rfc not found; install with: pip install xml2rfc" >&2
    exit 1
  fi
fi

for md in draft-*.md; do
  base="${md%.md}"
  echo "== $base =="
  kramdown-rfc "$md" 2>/dev/null > "$base.xml"
  xml2rfc "$base.xml" --text -o "$base.txt"
  echo "  -> $base.xml + $base.txt"
done
echo "== done =="