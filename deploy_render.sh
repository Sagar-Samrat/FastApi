#!/usr/bin/env bash
set -euo pipefail

# Simple script to trigger a Render deploy via API.
# Requires RENDER_API_KEY and RENDER_SERVICE_ID environment variables.

if [ -z "${RENDER_API_KEY:-}" ] || [ -z "${RENDER_SERVICE_ID:-}" ]; then
  echo "Error: RENDER_API_KEY and RENDER_SERVICE_ID must be set as environment variables."
  echo "Example: RENDER_API_KEY=xxx RENDER_SERVICE_ID=svc_xxx ./deploy_render.sh"
  exit 1
fi

echo "Triggering deploy for service: $RENDER_SERVICE_ID"
curl -s -X POST "https://api.render.com/v1/services/${RENDER_SERVICE_ID}/deploys" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -d '{}' | jq '.'

echo "Deploy triggered. Check Render dashboard for progress."
