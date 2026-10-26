#!/usr/bin/env bash
# Connect your Telegram bot to the autopilot. Run on YOUR Mac from the repo folder:
#
#   bash scripts/setup_telegram.sh
#
# Before running: in Telegram, message @BotFather, send /newbot, and keep the token it gives you.
# This script asks for the token (hidden), checks it, finds your chat when you press Start in
# your bot, saves TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID as GitHub secrets, and sends a test message.
# Nothing is printed or written to disk. Compatible with macOS bash 3.2.

set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"

bold() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
die()  { printf '\n\033[31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

command -v gh >/dev/null 2>&1 || die "GitHub CLI missing. Run: bash scripts/setup_autopilot.sh first."
command -v uv >/dev/null 2>&1 || die "uv missing. Run: bash scripts/setup_autopilot.sh first."
gh auth status >/dev/null 2>&1 || gh auth login --hostname github.com --git-protocol https --web
REPO="$(git remote get-url origin | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"
PY=(uv run --no-project --python 3.12 --quiet python)

json_get() {  # json_get '<python expression on d>'  (reads JSON on stdin)
  "${PY[@]}" -c "import json,sys; d=json.load(sys.stdin); v=$1; print('' if v is None else v)"
}

bold "Telegram bot token"
read -r -s -p "Paste the token from @BotFather (hidden): " TOKEN; echo
TOKEN="$(printf '%s' "$TOKEN" | tr -d '[:cntrl:]' | sed -e 's/\[20[01]~//g' -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
case "$TOKEN" in
  *[!A-Za-z0-9:_-]*|"") die "That doesn't look like a bot token (expected 123456:ABC...)." ;;
esac

ME="$(curl -fsS "https://api.telegram.org/bot${TOKEN}/getMe")" || die "Telegram rejected the token."
BOT="$(printf '%s' "$ME" | json_get "d['result']['username'] if d.get('ok') else None")"
[ -n "$BOT" ] || die "Telegram rejected the token."
echo "Bot found: @$BOT"

bold "Connect your chat"
echo "Open https://t.me/$BOT in Telegram and press START (or send it 'hi'). Waiting up to 2 minutes..."
CHAT_ID=""; NAME=""
for _ in $(seq 1 24); do
  UPD="$(curl -fsS "https://api.telegram.org/bot${TOKEN}/getUpdates?timeout=5&allowed_updates=%5B%22message%22%5D" || true)"
  CHAT_ID="$(printf '%s' "$UPD" | json_get "next((u['message']['chat']['id'] for u in reversed(d.get('result', [])) if u.get('message', {}).get('chat', {}).get('type') == 'private'), None)" 2>/dev/null || true)"
  if [ -n "$CHAT_ID" ]; then
    NAME="$(printf '%s' "$UPD" | json_get "next((u['message']['chat'].get('first_name', '') for u in reversed(d.get('result', [])) if u.get('message', {}).get('chat', {}).get('type') == 'private'), '')")"
    break
  fi
  sleep 5
done
[ -n "$CHAT_ID" ] || die "No message received. Press START in @$BOT, then run this again."

read -r -p "Found chat with '$NAME'. Is that you? [y/N] " ok
[ "$ok" = "y" ] || [ "$ok" = "Y" ] || die "Cancelled. Make sure only you have messaged the bot, then retry."

bold "Saving to GitHub ($REPO)"
printf '%s' "$TOKEN" | gh secret set TELEGRAM_BOT_TOKEN --repo "$REPO"
printf '%s' "$CHAT_ID" | gh secret set TELEGRAM_CHAT_ID --repo "$REPO"

curl -fsS -o /dev/null "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${CHAT_ID}" \
  --data-urlencode "text=✅ CyberBrief Studio is connected. Your weekly scripts will arrive here every Monday." \
  && echo "Test message sent: check Telegram."
TOKEN=""
bold "Done"
echo "Optional: start this week's batch now with:"
echo "  gh workflow run creator-weekly-scripts.yml --repo $REPO"
