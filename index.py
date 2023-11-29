import curses
import time
from random_word import RandomWords
from quote import quote

def generate_random_keyword():
    return RandomWords().get_random_word()

def generate_quote(keyword):
    return ''.join(quote(keyword, limit=1)[0]['quote'])

def display_text(stdscr, y, x, text, color_pair):
    stdscr.addstr(y, x, text, curses.color_pair(color_pair))

def handle_backspace(stdscr, typed_text):
    typed_text = typed_text[:-1]
    stdscr.move(2, 18)
    stdscr.clrtoeol()
    display_text(stdscr, 2, 18, typed_text, 2)
    stdscr.refresh()
    return typed_text

def handle_input_key(stdscr, typed_text, key, expected_text):
    typed_text += chr(key)

    for index, letter in enumerate(typed_text):
        correct_char = expected_text[index] if index < len(expected_text) else ' '
        text_color = 1 if letter == correct_char else 2
        display_text(stdscr, 2, 18 + index, letter, text_color)

    stdscr.refresh()
    return typed_text

def main(stdscr):
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    keyword = generate_random_keyword()
    expected_text = "The quick brown fox jumps over the lazy dog"
    typed_text = ""
    start_time = time.time()

    display_text(stdscr, 0, 5, expected_text, 1)
    display_text(stdscr, 2, 5, "Your input: ", 2)
    display_text(stdscr, 4, 5, "Typing Speed: ", 2)
    display_text(stdscr, 6, 5, "Words per Minute: ", 2)
    display_text(stdscr, 8, 5, "Time Elapsed: ", 2)

    while typed_text != expected_text:
        try:
            key = stdscr.getch()

            if key in {curses.KEY_BACKSPACE, 8}:
                typed_text = handle_backspace(stdscr, typed_text)

            elif chr(key).isalpha() or chr(key).isspace():
                typed_text = handle_input_key(stdscr, typed_text, key, expected_text)

            elif key in {ord('\n'), 27}:
                break

        except curses.error:
            pass

    end_time = time.time()
    elapsed_time = end_time - start_time
    words_per_minute = len(typed_text.split()) / elapsed_time * 60
    characters_per_minute = len(typed_text) / elapsed_time * 60

    display_text(stdscr, 4, 21, f"{characters_per_minute:.2f} CPM", 2)
    display_text(stdscr, 6, 23, f"{words_per_minute:.2f} WPM", 2)
    display_text(stdscr, 8, 18, f"{elapsed_time:.2f} seconds", 2)
    display_text(stdscr, 10, 5, "Press any key to exit.", 2)
    stdscr.refresh()

    stdscr.getch()

curses.wrapper(main)
