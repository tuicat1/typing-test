import curses
import time
from random_word import RandomWords
from quote import quote

def generate_random_keyword():
    r = RandomWords()
    return r.get_random_word()

def generate_quote(keyword):
    res = quote(keyword, limit=1)
    generated_quote = ""
    for i in range(len(res)):
        generated_quote = generate_quote + res[i]['quote']
    return generated_quote

def main(stdscr):
    # Initialize the screen
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Set up the typing test
    keyword = generate_random_keyword()
    # expected_text = generate_quote(keyword)
    # placeholder
    expected_text = "The quick brown fox jumps over the lazy dog"
    typed_text = ""
    start_time = time.time()

    # Set up the layout
    stdscr.addstr(0, 5, f"{expected_text}", curses.color_pair(1))
    stdscr.addstr(2, 5, "Your input: ", curses.color_pair(2))
    stdscr.addstr(4, 5, "Typing Speed: ", curses.color_pair(2))
    stdscr.addstr(6, 5, "Words per Minute: ", curses.color_pair(2))
    stdscr.addstr(8, 5, "Time Elapsed: ", curses.color_pair(2))

    # Main loop to get user input
    while typed_text != expected_text:
        try:
            key = stdscr.getch()

            # Check the value of the key (for debugging)
            print(f"Key pressed: {key}")

            # Handle Backspace key
            if key == curses.KEY_BACKSPACE or key == 8:
                if typed_text:
                    typed_text = typed_text[:-1]
                    # Clear the line and refresh
                    stdscr.move(2, 18)
                    stdscr.clrtoeol()
                    stdscr.addstr(2, 18, typed_text, curses.color_pair(2))
                    stdscr.refresh()

            # Handle alphanumeric characters and space
            elif chr(key).isalpha() or chr(key).isspace():
                typed_text += chr(key)

                # Display typed text with color coding
                for index, letter in enumerate(typed_text):
                    correct_char = expected_text[index] if index < len(expected_text) else ' '
                    text_color = curses.color_pair(1) if letter == correct_char else curses.color_pair(2)
                    stdscr.addstr(2, 18 + index, letter, text_color)

                stdscr.refresh()

            # Handle Enter key or Esc key to exit
            elif key == ord('\n') or key == 27:
                break

        except curses.error:
            pass

    # Calculate typing speed and display results
    end_time = time.time()
    elapsed_time = end_time - start_time
    words_per_minute = len(typed_text.split()) / elapsed_time * 60
    characters_per_minute = len(typed_text) / elapsed_time * 60

    stdscr.addstr(4, 21, f"{characters_per_minute:.2f} CPM", curses.color_pair(2))
    stdscr.addstr(6, 23, f"{words_per_minute:.2f} WPM", curses.color_pair(2))
    stdscr.addstr(8, 18, f"{elapsed_time:.2f} seconds", curses.color_pair(2))
    stdscr.addstr(10, 5, "Press Enter or Esc to exit.", curses.color_pair(2))
    stdscr.refresh()

    # Wait for a key press before exiting
    stdscr.getch()

curses.wrapper(main)
