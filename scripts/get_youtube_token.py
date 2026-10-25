"""One-time: get a YouTube refresh token. Run on YOUR computer (it opens a browser).

Easiest: run `bash scripts/setup_autopilot.sh`, which calls this script and stores the result
in GitHub for you. Manual use:

  pip install google-auth-oauthlib
  python scripts/get_youtube_token.py path/to/client_secret.json            # prints the values
  python scripts/get_youtube_token.py path/to/client_secret.json --out f.json  # writes them (mode 600)
"""
import argparse
import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]  # upload only — least privilege

ap = argparse.ArgumentParser()
ap.add_argument("client_secret_json")
ap.add_argument("--out", help="write the credentials to this file (mode 600) instead of printing them")
args = ap.parse_args()

flow = InstalledAppFlow.from_client_secrets_file(args.client_secret_json, SCOPES)
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
if not creds.refresh_token:
    raise SystemExit("Google did not return a refresh token. Remove the app's access at "
                     "myaccount.google.com/permissions and run this again.")

values = {
    "YT_CLIENT_ID": creds.client_id,
    "YT_CLIENT_SECRET": creds.client_secret,
    "YT_REFRESH_TOKEN": creds.refresh_token,
}
if args.out:
    fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as fh:
        json.dump(values, fh)
    print("YouTube authorization complete.")
else:
    print("\nSave these as secrets (never commit or share them):")
    for key, val in values.items():
        print(f"{key}={val}")
