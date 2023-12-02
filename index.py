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
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct input (green)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)    # Incorrect input (red)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Expected text (grey)

        self.keyword = self.generate_random_keyword()
        self.expected_text = self.generate_quote(self.keyword)[0:100]
        self.typed_text = ""
        self.start_time = None

        self.display_text(0, 5, self.expected_text, 1)
        self.display_expected_text()
        self.display_text(6, 5, "Words per Minute: ", 2)
        retry_message = "Press Tab to retry"
        self.display_text(10, 5, retry_message, 2)

    def generate_random_keyword(self):
        return RandomWords().get_random_word()

    def generate_quote(self, keyword):
        quotes = quote(keyword, limit=1)
        if quotes and quotes[0] and 'quote' in quotes[0]:
            return ''.join(quotes[0]['quote'])
        else:
            # Handle the case where the quote retrieval was unsuccessful
            return "The quick brown fox jumps over the lazy dog"


    def display_text(self, y, x, text, color_pair):
        self.stdscr.addstr(y, x, text, curses.color_pair(color_pair))

    def display_expected_text(self):
        for i, letter in enumerate(self.expected_text):
            text_color = 5  # grey
            self.display_text(2, 18 + i, letter, text_color)

        # Move the cursor to the beginning of the expected text
        self.stdscr.move(2, 18)
        
    def print_realtime_wpm(self):
        """Print realtime wpm during the test."""
        current_wpm = 0
        total_time = self.get_elapsed_minutes_since_first_keypress(self.start_time)
        if total_time != 0:
            words = self.typed_text.split()
            word_count = len(words)
            current_wpm = word_count / total_time

        self.stdscr.addstr(
            0,
            self.stdscr.getmaxyx()[1] - 14,
            f" {current_wpm:.2f} WPM ",
            curses.color_pair(2),  # CYAN
        )
        
    def get_elapsed_minutes_since_first_keypress(self, start_time):
        """Return the elapsed minutes since the first keypress."""
        return (time.time() - start_time) / 60


    def handle_backspace(self):
        if len(self.typed_text) > 0:
            # Move the cursor to the correct position before backspacing
            cursor_x = 18 + len(self.typed_text)
            self.stdscr.move(2, cursor_x)

            self.typed_text = self.typed_text[:-1]

            # Clear the current line and redisplay the expected text with the correct color
            self.stdscr.clrtoeol()
            for i, letter in enumerate(self.expected_text[:len(self.typed_text)]):
                text_color = 3 if letter == self.typed_text[i] else 4  # green or red
                self.display_text(2, 18 + i, letter, text_color)  # Highlight expected text

            # Update the expected text in grey up to the current typing position
            for i, letter in enumerate(self.expected_text[len(self.typed_text):], start=len(self.typed_text)):
                self.display_text(2, 18 + i, letter, 5)  # grey

            # Move the cursor to the end of the typed text
            self.stdscr.move(2, cursor_x - 1)  # Move the cursor back one place

            # Debugging: Print cursor position for verification
            print("Cursor Position After Backspace:", cursor_x - 1)

        # Refresh the display
        self.stdscr.refresh()

    def handle_input_key(self, key):
        if not self.start_time:
            self.start_time = time.time()

        if key in {curses.KEY_BACKSPACE, 8}:
            self.handle_backspace()
        elif chr(key).isalnum() or chr(key).isspace() or ord(chr(key)) in [59, 44, 46, 39, 63]:
            # Move the cursor one place ahead before handling the input
            cursor_x = 18 + len(self.typed_text)
            self.stdscr.move(2, cursor_x + 1)
            self.handle_valid_input(chr(key), key)
            self.print_realtime_wpm()


            
    def handle_valid_input(self, input_char, key):
        index = len(self.typed_text)
        correct_char = self.expected_text[index] if index < len(self.expected_text) else ' '

        if input_char == correct_char:
            text_color = 3  # green for correct input
        else:
            text_color = 4 if input_char != ' ' or correct_char.isspace() else 4  # red for incorrect input

        self.typed_text += input_char
        self.display_text(2, 18 + index, correct_char, text_color)  # Highlight expected text
        self.update_typing_speed()

    def update_typing_speed(self):
        if self.typed_text == self.expected_text:
            elapsed_time = time.time() - self.start_time
            words_per_minute = len(self.typed_text.split()) / elapsed_time * 60
            self.display_text(6, 23, f"{words_per_minute:.2f} WPM", 2)

    def run(self):
        while True:
            try:
                key = self.stdscr.getch()

                if key == 9:  # Check for the tab key
                    self.reset_typing_test()
                elif key in {curses.KEY_BACKSPACE, 8}:
                    self.handle_backspace()
                elif chr(key).isalpha() or chr(key).isspace() or ord(chr(key)) in [59, 44, 46, 39, 63]:
                    self.handle_input_key(key)
                elif key in {ord('\n'), 27}:
                    break

            except curses.error:
                pass
            
        end_time = time.time()
        elapsed_time = end_time - (self.start_time or end_time)
        words_per_minute = len(self.typed_text.split()) / elapsed_time * 60

        self.display_text(6, 23, f"{words_per_minute:.2f} WPM", 2)
        self.display_text(10, 5, "Press any key to exit.", 2)
        self.stdscr.refresh()

        self.stdscr.getch()

    def reset_typing_test(self):
        # Reset all relevant variables and display
        self.typed_text = ""
        self.start_time = None

        self.display_text(2, 18, " " * len(self.expected_text), 5)  # Clear typed text
        self.display_expected_text()
        self.display_text(6, 23, " " * 10, 2)  # Clear WPM display

def main(stdscr):
    curses.curs_set(1)  # Set cursor visibility to normal
    typing_speed_test = TypingSpeedTest(stdscr)
    typing_speed_test.run()

curses.wrapper(main)
