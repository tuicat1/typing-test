import curses
import time
from random_word import RandomWords
from quote import quote

class TypingSpeedTest:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

        self.keyword = self.generate_random_keyword()
        self.expected_text = "The quick brown fox jumps over the lazy dog"
        self.typed_text = ""
        self.start_time = None

        self.display_text(0, 5, self.expected_text, 1)
        self.display_text(4, 5, "Typing Speed: ", 2)
        self.display_text(6, 5, "Words per Minute: ", 2)
        self.display_text(8, 5, "Time Elapsed: ", 2)

    def generate_random_keyword(self):
        return RandomWords().get_random_word()

    def generate_quote(self, keyword):
        return ''.join(quote(keyword, limit=1)[0]['quote'])

    def display_text(self, y, x, text, color_pair):
        self.stdscr.addstr(y, x, text, curses.color_pair(color_pair))

    def handle_backspace(self):
        self.typed_text = self.typed_text[:-1]
        self.stdscr.move(2, 18)
        self.stdscr.clrtoeol()
        self.display_text(2, 18, self.typed_text, 2)
        self.stdscr.refresh()

    def handle_input_key(self, key):
        if not self.start_time:
            self.start_time = time.time()

        self.typed_text += chr(key)

        for index, letter in enumerate(self.typed_text):
            correct_char = self.expected_text[index] if index < len(self.expected_text) else ' '
            text_color = 1 if letter == correct_char else 2
            self.display_text(2, 18 + index, letter, text_color)

        self.stdscr.refresh()

        if self.typed_text == self.expected_text:
            elapsed_time = time.time() - self.start_time
            words_per_minute = len(self.typed_text.split()) / elapsed_time * 60
            self.display_text(6, 23, f"{words_per_minute:.2f} WPM", 2)

    def run(self):
        while self.typed_text != self.expected_text:
            try:
                key = self.stdscr.getch()

                if key in {curses.KEY_BACKSPACE, 8}:
                    self.handle_backspace()

                elif chr(key).isalpha() or chr(key).isspace():
                    self.handle_input_key(key)

                elif key in {ord('\n'), 27}:
                    break

            except curses.error:
                pass

        end_time = time.time()
        elapsed_time = end_time - (self.start_time or end_time)
        words_per_minute = len(self.typed_text.split()) / elapsed_time * 60

        self.display_text(4, 21, f"{len(self.typed_text) / elapsed_time * 60:.2f} CPM", 2)
        self.display_text(6, 23, f"{words_per_minute:.2f} WPM", 2)
        self.display_text(8, 18, f"{elapsed_time:.2f} seconds", 2)
        self.display_text(10, 5, "Press any key to exit.", 2)
        self.stdscr.refresh()

        self.stdscr.getch()


def main(stdscr):
    typing_speed_test = TypingSpeedTest(stdscr)
    typing_speed_test.run()


curses.wrapper(main)
