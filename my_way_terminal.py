#!/usr/bin/env python3
"""Neon Sakura terminal lyric display - Frank Sinatra My Way (looping) - word by word."""

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
    ("And now, the end is near", CYAN),
    ("And so I face, the final curtain", PURPLE),
    ("My friend, I'll say it clear", GLOW),
    ("I'll state my case, of which I'm certain", WHITE),
    ("", WHITE),
    ("I've lived a life that's full", PINK),
    ("I've traveled each and every highway", CYAN),
    ("And more, much more than this", PURPLE),
    ("I did it my way", BOLD + GLOW),
    ("", WHITE),
    ("What is a man, what has he got?", BOLD + PINK),
    ("If not himself, then he has naught", CYAN),
    ("To say the things he truly feels", PURPLE),
    ("And not the words of one who kneels", WHITE),
    ("The record shows I took the blows", GLOW),
    ("And did it my way", BOLD + PINK),
]


def clear_screen():
    os.system("clear")


def type_words(line, color, word_delay=0.5):
    """Type each word with delay between words."""
    if not line.strip():
        print()
        time.sleep(0.3)
        return
    
    words = line.split()
    for word in words:
        sys.stdout.write(color + word + " " + RESET)
        sys.stdout.flush()
        time.sleep(word_delay)
    print()
    time.sleep(0.2)


def main():
    iteration = 0
    try:
        while True:
            clear_screen()
            if iteration > 0:
                time.sleep(1.5)
            
            title = "\n" + " " * 10 + "NEON SAKURA - MY WAY"
            print(BOLD + PINK + title + RESET)
            print(BOLD + CYAN + " " * 8 + "Frank Sinatra" + RESET)
            time.sleep(0.8)
            print()

            for line, color in LINES:
                type_words(line, color, word_delay=0.5)

            print("\n" + " " * 12 + BOLD + CYAN + "(looping... press Ctrl+C to exit)" + RESET)
            time.sleep(1)
            iteration += 1

    except KeyboardInterrupt:
        clear_screen()
        print(BOLD + PINK + "\nI did it my way.\n" + RESET)
        sys.exit(0)


if __name__ == "__main__":
    main()
