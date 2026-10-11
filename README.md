# 3D Sakura Spring Wallpaper

A lightweight Linux-safe wallpaper generator for Arch Linux. It creates a soft 3D-style spring sakura scene in a pastel pink / plum palette.

Features:
- 3D-ish layered sakura blossoms
- spring sky gradient
- stylized branches and petals
- generated PNG wallpaper
- easy Arch Linux wallpaper install via `feh`

## Requirements

Python 3 and Pillow:

```bash
python3 -m pip install -r requirements.txt
```

## Generate wallpaper

```bash
python3 generate_wallpaper.py
```

This creates:

```text
output/sakura_wallpaper.png
```

## Set as wallpaper on Arch Linux

If `feh` is installed:

```bash
./set_wallpaper.sh
```

If not, open the image manually in your wallpaper manager.

## Files

- `generate_wallpaper.py` — renders the wallpaper
- `set_wallpaper.sh` — generates and applies the wallpaper if possible
- `output/` — generated image output
