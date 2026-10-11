#!/usr/bin/env python3
"""Neon Sakura terminal lyric display for a short My Way style excerpt."""

import os
import sys
import time

RESET = "\033[0m"
BOLD = "\033[1m"
PINK = "\033[38;5;213m"
PURPLE = "\033[38;5;177m"
CYAN = "\033[38;5;117m"
WHITE = "\033[38;5;255m"
GLOW = "\033[38;5;225m"

LINES = [
    ("MY WAY", BOLD + PINK),
    ("I've had my share of sand", WHITE),
    ("and tears and trouble", CYAN),
    ("but I've lived each moment", PURPLE),
    ("as it came", GLOW),
    ("I did it my way", BOLD + PINK),
]


def clear_screen():
    os.system("clear")


def type_line(line, color, delay=0.04):
    for ch in line:
        sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    time.sleep(0.18)


def main():
    clear_screen()
    title = "\n" + " " * 10 + "NEON SAKURA TERMINAL"
    print(BOLD + PINK + title + RESET)
    time.sleep(0.7)

    for line, color in LINES:
        type_line(line, color, delay=0.045)

    print("\n" + " " * 12 + BOLD + CYAN + "press Ctrl+C to exit" + RESET)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(BOLD + PINK + "\nGood night, dear friend." + RESET)
        sys.exit(0)
