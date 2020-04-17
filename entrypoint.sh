#!/usr/bin/env sh
set -e

if [ -n "$TOKEN_PICKLE" ]; then
  echo "$TOKEN_PICKLE" | base64 -d > token.pickle
fi

exec "$@"
