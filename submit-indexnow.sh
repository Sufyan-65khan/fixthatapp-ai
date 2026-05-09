#!/bin/bash
# Pings IndexNow (Bing, Yandex, DuckDuckGo, Seznam) with every URL in sitemap.xml.
# Run after every push that adds or significantly updates pages.
# Usage: bash submit-indexnow.sh

KEY="6bfa5b43c098b6cfe04c89824c23d796"
HOST="www.fixthatapp.com"
KEY_LOCATION="https://www.fixthatapp.com/${KEY}.txt"
SITEMAP="sitemap.xml"

if [ ! -f "$SITEMAP" ]; then
  echo "sitemap.xml not found in current directory"
  exit 1
fi

# Extract URLs from sitemap
URLS=$(grep -oE '<loc>[^<]+</loc>' "$SITEMAP" | sed 's|<loc>||;s|</loc>||')
COUNT=$(echo "$URLS" | wc -l)

# Build JSON urlList
URL_JSON=$(echo "$URLS" | awk 'BEGIN{ORS=""; print "["} {if(NR>1) print ","; printf "\"%s\"", $0} END{print "]"}')

PAYLOAD=$(printf '{"host":"%s","key":"%s","keyLocation":"%s","urlList":%s}' \
  "$HOST" "$KEY" "$KEY_LOCATION" "$URL_JSON")

echo "Submitting $COUNT URLs to IndexNow..."
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$PAYLOAD")

HTTP_STATUS=$(echo "$RESPONSE" | grep -oE 'HTTP_STATUS:[0-9]+' | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS:/d')

echo "Response: HTTP $HTTP_STATUS"
[ -n "$BODY" ] && echo "Body: $BODY"

case "$HTTP_STATUS" in
  200|202) echo "Success. URLs queued for indexing." ;;
  400) echo "Bad request. Check JSON payload." ;;
  403) echo "Key file not reachable at $KEY_LOCATION. Check it's deployed and publicly accessible." ;;
  422) echo "URLs rejected. Check they all match the host." ;;
  429) echo "Rate limited. Wait and retry." ;;
  *) echo "Unexpected status. Check IndexNow docs." ;;
esac
