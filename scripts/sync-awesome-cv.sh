#!/usr/bin/env bash
set -euo pipefail

source_pdf="${1:-../awesome-cv/cv/cv.pdf}"
target_pdf="assets/pdf/academic-cv.pdf"
preview_prefix="assets/img/cv/academic-cv"

if [[ ! -f "$source_pdf" ]]; then
  echo "Missing Awesome-CV PDF: $source_pdf" >&2
  exit 1
fi

mkdir -p "$(dirname "$target_pdf")"
cp "$source_pdf" "$target_pdf"
echo "Synced $source_pdf -> $target_pdf"

if command -v pdftoppm >/dev/null 2>&1; then
  mkdir -p "$(dirname "$preview_prefix")"
  rm -f "${preview_prefix}"-*.png
  pdftoppm -png -r 144 "$target_pdf" "$preview_prefix"
  echo "Generated ${preview_prefix}-*.png"
else
  echo "pdftoppm not found; skipped CV preview image generation" >&2
fi
