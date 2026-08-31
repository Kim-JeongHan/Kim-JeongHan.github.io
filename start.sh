#!/usr/bin/env bash

set -euo pipefail

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
image_name="kim-jeonghan-blog-dev"
jekyll_arguments=(--incremental)

if (( $# > 1 )); then
  printf 'Usage: %s [--all]\n' "$0" >&2
  exit 2
fi

if [[ ${1:-} == "--all" ]]; then
  jekyll_arguments=()
elif [[ -n ${1:-} ]]; then
  printf 'Usage: %s [--all]\n' "$0" >&2
  exit 2
fi

docker build --tag "$image_name" "$script_directory"

exec docker run --rm --interactive --tty \
  --user "$(id -u):$(id -g)" \
  --publish 4000:4000 \
  --volume "$script_directory:/srv/jekyll" \
  --workdir /srv/jekyll \
  "$image_name" \
  "${jekyll_arguments[@]}"
