#!/usr/bin/env bash
# Chrome'u CDP acik ve ayri bir profille baslatir.
# Acilan pencerede sahibinden.com'a normal sekilde gir; dogrulama cikarsa kendin gec.
# Sonra: emlakarama fetch <url> --cdp
set -euo pipefail
PORT="${1:-9222}"
PROFILE="${EMLAKARAMA_CHROME_PROFILE:-$HOME/.emlakarama-chrome}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || CHROME="$(command -v google-chrome || command -v chromium || true)"
[ -n "$CHROME" ] || { echo "Chrome bulunamadi." >&2; exit 1; }
echo "CDP port : $PORT"
echo "Profil   : $PROFILE"
exec "$CHROME" --remote-debugging-port="$PORT" --user-data-dir="$PROFILE" \
  "https://www.sahibinden.com"
