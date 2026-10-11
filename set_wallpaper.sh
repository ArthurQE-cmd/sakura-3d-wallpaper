#!/usr/bin/env bash
set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

python3 generate_wallpaper.py --output output/sakura_wallpaper.png

if command -v feh >/dev/null 2>&1; then
  feh --bg-fill output/sakura_wallpaper.png
else
  echo "Wallpaper generated at: $script_dir/output/sakura_wallpaper.png"
  echo "Install feh to set it automatically: sudo pacman -S feh"
fi
