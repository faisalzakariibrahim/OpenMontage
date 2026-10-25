#!/usr/bin/env bash
# One-command autopilot setup. Run on YOUR Mac, from the repo folder:
#
#   bash scripts/setup_autopilot.sh
#
# It will:
#   1. install uv (Python runner) and the GitHub CLI if missing, and sign you in to GitHub
#   2. open Google sign-in and get a YouTube upload token (scope: youtube.upload only)
#   3. create the `social-publish` GitHub Environment with you as required reviewer
#   4. store the YouTube token as Environment secrets, and your API keys as repo secrets
#   5. optionally start a dry-run of the Autopilot workflow
#
# Secrets go straight from this terminal to GitHub's encrypted secret store. They are never
# printed, never passed on a command line (stdin only), and the temp file is deleted on exit.
# Compatible with the bash 3.2 that ships with macOS.

set -euo pipefail
cd "$(dirname "$0")/.."

ENV_NAME="social-publish"
API_KEYS="ANTHROPIC_API_KEY OPENAI_API_KEY PEXELS_API_KEY FAL_KEY"

bold() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
die()  { printf '\n\033[31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }
ask()  { local reply; read -r -p "$1 [y/N] " reply; [ "$reply" = "y" ] || [ "$reply" = "Y" ]; }

TMP_DIR="$(mktemp -d)"
chmod 700 "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

# ---------------------------------------------------------------- 1. tools
bold "Checking tools"
export PATH="$HOME/.local/bin:$PATH"
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv (brings its own Python)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
command -v uv >/dev/null 2>&1 || die "uv did not install. Open a new terminal and run this script again."
PY=(uv run --no-project --python 3.12 --quiet)

if ! command -v gh >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo "Installing GitHub CLI with Homebrew..."
    brew install gh
  else
    echo "Installing GitHub CLI into ~/.local/bin..."
    arch="$(uname -m)"; [ "$arch" = "x86_64" ] && arch="amd64"
    url="$("${PY[@]}" python -c '
import json, sys, urllib.request
rel = json.load(urllib.request.urlopen("https://api.github.com/repos/cli/cli/releases/latest"))
want = "macOS_" + sys.argv[1] + ".zip"
print(next(a["browser_download_url"] for a in rel["assets"] if a["name"].endswith(want)))
' "$arch")"
    curl -fsSL "$url" -o "$TMP_DIR/gh.zip"
    unzip -q "$TMP_DIR/gh.zip" -d "$TMP_DIR/gh"
    mkdir -p "$HOME/.local/bin"
    cp "$TMP_DIR"/gh/*/bin/gh "$HOME/.local/bin/gh"
  fi
fi
command -v gh >/dev/null 2>&1 || die "GitHub CLI did not install. Install it from https://cli.github.com and re-run."

if ! gh auth status >/dev/null 2>&1; then
  bold "Sign in to GitHub (a browser window will open)"
  gh auth login --hostname github.com --git-protocol https --web
fi

REMOTE="$(git remote get-url origin)"
REPO="$(printf '%s' "$REMOTE" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"
gh repo view "$REPO" >/dev/null 2>&1 || die "Can't access $REPO with your GitHub login."
ME_ID="$(gh api user --jq .id)"
ME="$(gh api user --jq .login)"
echo "Repo: $REPO   GitHub user: $ME"

# ---------------------------------------------------------------- 2. YouTube token
bold "YouTube authorization"
shopt -s nullglob
secrets_files=("$HOME"/Downloads/client_secret*.json)
shopt -u nullglob
if [ "${1:-}" != "" ]; then
  CLIENT_JSON="$1"
elif [ "${#secrets_files[@]}" -eq 1 ]; then
  CLIENT_JSON="${secrets_files[0]}"
elif [ "${#secrets_files[@]}" -eq 0 ]; then
  die "No client_secret*.json in ~/Downloads. In Google Cloud: Credentials -> your Desktop OAuth client -> Download JSON."
else
  die "Found ${#secrets_files[@]} client_secret*.json files in ~/Downloads. Delete the old ones (keep the newest) and re-run."
fi
echo "Using $(basename "$CLIENT_JSON")"
echo "A browser opens. Sign in with the account that owns your YouTube channel and pick that channel."
echo "If Google says the app isn't verified: Advanced -> Go to ... (it's your own app)."

TOKEN_FILE="$TMP_DIR/yt.json"
"${PY[@]}" --with google-auth-oauthlib python scripts/get_youtube_token.py "$CLIENT_JSON" --out "$TOKEN_FILE"
[ -s "$TOKEN_FILE" ] || die "No YouTube token was produced."

# ---------------------------------------------------------------- 3. Environment
bold "Creating the '$ENV_NAME' environment (you approve every upload)"
printf '{"reviewers":[{"type":"User","id":%s}],"prevent_self_review":false,"deployment_branch_policy":{"protected_branches":false,"custom_branch_policies":true}}' "$ME_ID" \
  | gh api -X PUT "repos/$REPO/environments/$ENV_NAME" --input - >/dev/null
gh api -X POST "repos/$REPO/environments/$ENV_NAME/deployment-branch-policies" \
  -f name=main -f type=branch >/dev/null 2>&1 || true   # already exists is fine
echo "Done: uploads now wait for $ME to approve, and only from the main branch."

# ---------------------------------------------------------------- 4. Secrets
bold "Saving YouTube credentials as environment secrets"
for key in YT_CLIENT_ID YT_CLIENT_SECRET YT_REFRESH_TOKEN; do
  "${PY[@]}" python -c 'import json,sys; sys.stdout.write(json.load(open(sys.argv[1]))[sys.argv[2]])' "$TOKEN_FILE" "$key" \
    | gh secret set "$key" --env "$ENV_NAME" --repo "$REPO"
done
rm -f "$TOKEN_FILE"

bold "API keys (typing is hidden; press Enter to skip one you've already saved)"
existing="$(gh secret list --repo "$REPO" --json name --jq '.[].name' 2>/dev/null || true)"
for key in $API_KEYS; do
  if printf '%s\n' "$existing" | grep -qx "$key"; then note=" (already saved — Enter keeps it)"; else note=""; fi
  read -r -s -p "  $key$note: " value; echo
  if [ -n "$value" ]; then
    printf '%s' "$value" | gh secret set "$key" --repo "$REPO"
    echo "    saved"
  fi
  value=""
done
gh variable set AUTO_PUBLISH --body false --repo "$REPO" >/dev/null
echo "AUTO_PUBLISH=false (YouTube uploads stay private for review)"

# ---------------------------------------------------------------- 5. cleanup + test
if ask "Delete $(basename "$CLIENT_JSON") from Downloads now? GitHub has what it needs."; then
  rm -f "$CLIENT_JSON" && echo "Deleted."
fi

bold "Setup complete"
missing=""
saved="$(gh secret list --repo "$REPO" --json name --jq '.[].name' 2>/dev/null || true)"
for key in $API_KEYS; do printf '%s\n' "$saved" | grep -qx "$key" || missing="$missing $key"; done
if [ -n "$missing" ]; then
  echo "Still missing:$missing. Re-run this script when you have them (the YouTube step can be repeated safely)."
  exit 0
fi

if ask "Start a dry run now? It makes one real video (~\$1-4) but does not upload."; then
  gh workflow run autopilot-short.yml --repo "$REPO" -f dry_run=true
  sleep 5
  gh run list --repo "$REPO" --workflow autopilot-short.yml --limit 1 --json url --jq '.[0].url'
  echo "Watch it there. When it finishes, download the artifact to see the video."
fi
