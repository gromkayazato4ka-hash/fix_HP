#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

ADDON_DIR="zbrush_highpoly_repair"
ZIP_NAME="zbrush_highpoly_repair_release.zip"

rm -f "$ZIP_NAME"

zip -r "$ZIP_NAME" "$ADDON_DIR" \
  -x '*/__pycache__/*' \
  -x '*.pyc' \
  -x '*/.DS_Store' \
  -x '*/.gitignore'

echo "Built $ZIP_NAME"
