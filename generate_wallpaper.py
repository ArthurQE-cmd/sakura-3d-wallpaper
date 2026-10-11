#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def draw_gradient_background(draw, width: int, height: int):
    top_color = (28, 24, 44)
    mid_color = (97, 61, 86)
    bottom_color = (241, 193, 214)

    for y in range(height):
        ratio = y / max(height - 1, 1)
        if ratio < 0.55:
            r = int(lerp(top_color[0], mid_color[0], ratio / 0.55))
            g = int(lerp(top_color[1], mid_color[1], ratio / 0.55))
            b = int(lerp(top_color[2], mid_color[2], ratio / 0.55))
        else:
            r = int(lerp(mid_color[0], bottom_color[0], (ratio - 0.55) / 0.45))
            g = int(lerp(mid_color[1], bottom_color[1], (ratio - 0.55) / 0.45))
            b = int(lerp(mid_color[2], bottom_color[2], (ratio - 0.55) / 0.45))
        draw.line((0, y, width, y), fill=(r, g, b))


def add_sun_glow(draw, width: int, height: int):
    cx = int(width * 0.8)
    cy = int(height * 0.2)
    radius = int(min(width, height) * 0.22)
    for i in range(12, 0, -1):
        alpha = 255 - (i * 12)
        color = (255, 220, 230, alpha)
        draw.ellipse((cx - radius * i / 12, cy - radius * i / 12,
                      cx + radius * i / 12, cy + radius * i / 12), outline=color)

    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(255, 229, 235, 160))


def add_haze(draw, width: int, height: int):
    for x, y, radius, alpha in [
        (width * 0.22, height * 0.28, width * 0.18, 80),
        (width * 0.62, height * 0.34, width * 0.22, 74),
        (width * 0.45, height * 0.48, width * 0.26, 64),
    ]:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 255, 255, alpha))


def draw_branch(draw, points, color, thickness):
    draw.line(points, fill=color, width=thickness)


def branch_system(draw):
    dark = (66, 46, 58)
    branches = [
        ((200, 1200), (420, 930), (620, 980), (960, 810), (1180, 700), (1610, 780)),
        ((700, 1200), (860, 980), (1100, 940), (1420, 840), (1750, 900)),
        ((1200, 1210), (1360, 1010), (1550, 960), (1800, 1020)),
    ]

    for pts in branches:
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            draw_branch(draw, (x1, y1, x2, y2), dark, 9)

            # fine twigs
            if i < len(pts) - 2:
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                twig_len = 80
                angle = 0.6 if i % 2 == 0 else -0.5
                tx = int(mx + twig_len * (1 if i % 2 == 0 else -1) * 0.6)
                ty = int(my + twig_len * angle)
                draw_branch(draw, (mx, my, tx, ty), dark, 4)


def blossom_petal(draw, x, y, radius, fill_color, outline_color, rotation=0):
    petal = [
        (0, -radius),
        (radius * 0.65, -radius * 0.2),
        (radius, radius * 0.5),
        (0, radius),
        (-radius, radius * 0.5),
        (-radius * 0.65, -radius * 0.2),
    ]

    transformed = []
    for px, py in petal:
        xr = px * 0.95
        yr = py
        x_rot = xr * __import__('math').cos(rotation) - yr * __import__('math').sin(rotation)
        y_rot = xr * __import__('math').sin(rotation) + yr * __import__('math').cos(rotation)
        transformed.append((x + x_rot, y + y_rot))

    draw.polygon(transformed, fill=fill_color, outline=outline_color)


def blossom_cluster(draw, cx, cy, base_size, depth=0):
    pink = (255, 199, 219)
    rose = (234, 113, 161)
    dark_pink = (129, 61, 94)

    for i in range(8):
        angle = (3.14159 * 2 / 8) * i
        petal_size = base_size + depth * 3
        x = cx + __import__('math').cos(angle) * (base_size * 0.9)
        y = cy + __import__('math').sin(angle) * (base_size * 0.75)
        blossom_petal(draw, x, y, petal_size, pink, dark_pink, rotation=angle * 0.5)

    draw.ellipse((cx - base_size * 0.5, cy - base_size * 0.5,
                  cx + base_size * 0.5, cy + base_size * 0.5),
                 fill=rose, outline=(136, 80, 110))


def add_petals(draw, width: int, height: int):
    for i in range(180):
        x = int(__import__('random').random() * width)
        y = int(__import__('random').random() * height)
        scale = __import__('random').uniform(2.5, 10)
        alpha = int(__import__('random').uniform(60, 180))
        color = (255, 206, 224, alpha)

        if y < height * 0.72:
            shape = [
                (x, y),
                (x + scale * 0.6, y - scale),
                (x + scale * 1.1, y),
                (x + scale * 0.6, y + scale * 1.0),
            ]
            draw.polygon(shape, fill=color)


def add_sakura_blossoms(draw, width: int, height: int):
    for x in range(90, width - 60, 150):
        for y in range(280, height - 150, 160):
            if (x + y) % 260 == 0:
                offset = 18
                blossom_cluster(draw, x + offset, y + 10, 24, depth=1)
                blossom_cluster(draw, x + 120, y + 40, 18, depth=2)
                blossom_cluster(draw, x - 80, y + 90, 22, depth=0)


def add_foreground_ground(draw, width: int, height: int):
    ground_y = int(height * 0.83)
    for y in range(ground_y, height + 8):
        alpha = clamp(int(255 * (1 - (y - ground_y) / max(height - ground_y, 1))), 20, 120)
        shade = (94, 120, 104, alpha)
        draw.line((0, y, width, y), fill=shade, width=2)

    # a subtle lower field
    draw.rectangle((0, ground_y, width, height), fill=(175, 197, 177, 120))


def render_wallpaper(output_path: Path, width: int = 2560, height: int = 1440):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw_gradient_background(draw, width, height)
    add_sun_glow(draw, width, height)
    add_haze(draw, width, height)
    branch_system(draw)
    add_sakura_blossoms(draw, width, height)
    add_petals(draw, width, height)
    add_foreground_ground(draw, width, height)

    # soft glow of the sky
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for i in range(10):
        radius = width * (0.18 + i * 0.07)
        glow_draw.ellipse((width * 0.12 - radius, height * 0.18 - radius,
                           width * 0.12 + radius, height * 0.18 + radius),
                          outline=(255, 235, 244, 20 - i * 2))
    image = Image.alpha_composite(image, glow)

    image = image.filter(ImageFilter.GaussianBlur(0.5))
    image.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate a 3D Sakura Spring wallpaper.")
    parser.add_argument("--output", type=str, default="output/sakura_wallpaper.png", help="Output file path")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    render_wallpaper(output)
    print(f"Wallpaper saved to {output.resolve()}")


if __name__ == "__main__":
    main()

