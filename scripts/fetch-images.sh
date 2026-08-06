#!/usr/bin/env bash
#
# Pull the founder photo and client logos off Oscar's Wix CDN and host them
# in this repo instead, then repoint every page at the local copies.
#
# Why: the site currently loads those images from static.wixstatic.com. When
# the old Wix site is taken down, those URLs stop working and the logos and
# founder photo disappear. Running this once removes that dependency.
#
# Usage:   bash scripts/fetch-images.sh
# Safe to re-run. Re-downloads nothing that is already present unless -f.
#
set -euo pipefail

cd "$(dirname "$0")/.."
CDN="https://static.wixstatic.com/media"
IMG="assets/img"
FORCE="${1:-}"

mkdir -p "$IMG/clients"

# local_path|cdn_filename
ASSETS=(
  "$IMG/oscar-cancino.jpg|94493f_c55f573e540c4e2f833e636db76b9985~mv2.jpg"
  "$IMG/clients/vincero.png|94493f_9b8fefa27fdb4c1fbe4af7fa2f279020~mv2.png"
  "$IMG/clients/craftmix.png|94493f_27655ebc461446a09e292ea352749812~mv2.png"
  "$IMG/clients/super-fiber.jpg|94493f_29518f81bf744da6b2cd99e9fa6f4ea8~mv2.jpg"
  "$IMG/clients/lusso-cloud.png|94493f_f7db1bc04c4b4baebe8741a312a3b156~mv2.png"
  "$IMG/clients/better-with-age.png|94493f_f72cf45097bd490f905d7d25cf45bdab~mv2.png"
  "$IMG/clients/day-out.png|94493f_0d335c03c5e74f21ac92dfd41dc812b6~mv2.png"
  "$IMG/clients/kayode.png|94493f_605e242e19be468b9bcc9cd5ba8a277d~mv2.png"
  "$IMG/clients/the-vin-store.png|94493f_b436f97fa2f94875a85dd4ffab7ff211~mv2.png"
  "$IMG/clients/vk-energy-bar.png|94493f_c46243acffe744688df97435dc59ca1a~mv2.png"
)

echo "Downloading ${#ASSETS[@]} images from the Wix CDN..."
failed=0
for entry in "${ASSETS[@]}"; do
  local_path="${entry%%|*}"
  cdn_file="${entry##*|}"

  if [[ -s "$local_path" && "$FORCE" != "-f" ]]; then
    printf '  skip (already here)  %s\n' "$local_path"
    continue
  fi

  if curl -fsSL --max-time 60 -o "$local_path.tmp" "$CDN/$cdn_file"; then
    # Reject anything that is not actually an image (error pages, redirects)
    if [[ -s "$local_path.tmp" ]] && file -b --mime-type "$local_path.tmp" | grep -q '^image/'; then
      mv "$local_path.tmp" "$local_path"
      printf '  ok  %-42s %s bytes\n' "$local_path" "$(wc -c < "$local_path")"
    else
      rm -f "$local_path.tmp"
      printf '  FAILED (not an image)  %s\n' "$local_path"
      failed=$((failed + 1))
    fi
  else
    rm -f "$local_path.tmp"
    printf '  FAILED (download)  %s\n' "$local_path"
    failed=$((failed + 1))
  fi
done

if (( failed > 0 )); then
  echo
  echo "$failed image(s) could not be downloaded. Nothing was repointed."
  echo "The pages still load those images from the Wix CDN, so the site is unchanged."
  exit 1
fi

echo
echo "Repointing pages at the local copies..."
changed=0
while IFS= read -r page; do
  before="$(md5sum "$page" | cut -d' ' -f1)"
  for entry in "${ASSETS[@]}"; do
    local_path="${entry%%|*}"
    cdn_file="${entry##*|}"
    # /assets/img/... is the root-absolute form the pages use
    sed -i "s#https://static\.wixstatic\.com/media/${cdn_file}#/${local_path}#g" "$page"
  done
  after="$(md5sum "$page" | cut -d' ' -f1)"
  [[ "$before" != "$after" ]] && changed=$((changed + 1))
done < <(find . -name '*.html' -not -path './node_modules/*' -not -path './.git/*')

remaining="$(grep -rl 'static\.wixstatic\.com' --include='*.html' . 2>/dev/null | wc -l | tr -d ' ')"

echo "  updated $changed page(s)"
echo "  pages still referencing the Wix CDN: $remaining"
echo
if [[ "$remaining" == "0" ]]; then
  echo "Done. The site no longer depends on the Wix CDN."
  echo "Commit the new files:  git add assets/img *.html services locations resources && git commit"
else
  echo "Some references remain. Check them before taking the Wix site down."
  exit 1
fi
