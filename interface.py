import time
import curses
import stats
from person import Person


class Interface:

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.nocbreak()
        self.stdscr.keypad(True)

    def init_interface(self):
        self.init_curses()
        self.init_curses_colors()
        self.get_console_size()
        self.is_curses_initialized = True

    def init_curses(self):
        self.stdscr.scrollok(True)
        curses.start_color()
        curses.curs_set(0)

    def init_curses_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def get_console_size(self):
        self.size = self.stdscr.getmaxyx()
        self.console_x = self.size[0]
        self.console_y = self.size[1]

    def refresh_display(self):
        self.stdscr.refresh()

    def print_person(self, id, person):
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(id + 2, 0, '[')

        if person.children > 3:
            person.children = 3
        if person.age > person.life_expectancy:
            person.age = person.life_expectancy

        if person.gender == 'Male':
            self.stdscr.addstr(
                id + 2, stats.AGE_LIMIT, f'] Gender: {person.gender}, Children: {person.children}, Age: {person.age}')
        elif person.gender == 'Female':
            self.stdscr.addstr(
                id + 2, stats.AGE_LIMIT, f'] Gender: {person.gender}, Children: {person.children}, Age: {person.age}')

        self.stdscr.attron(curses.color_pair(7))
        self.stdscr.addstr(id + 2, person.age - 1, ' ')
        self.stdscr.addstr(id + 2, person.age, '#')

    def print_person_death(self, id, person):
        if person.life_expectancy == person.age:
            death_cause = 'natural'
            self.stdscr.attron(curses.color_pair(1))
        else:
            death_cause = 'accident'
            self.stdscr.attron(curses.color_pair(3))

        self.stdscr.addstr(id + 2, 0, '[')
        self.stdscr.addstr(id + 2, stats.AGE_LIMIT, f'] Death: {death_cause}')

    def print_info(self):
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(
            0,
            0,
            f'Starting population: {stats.STARTING_POPULATION_SIZE} \
            || Birth ratio: {stats.BIRTH_RATIO_YEARLY} \
            || Birth age: {stats.BIRTH_MIN_AGE} - {stats.BIRTH_MAX_AGE} \
            || Accident ratio: {stats.ACCIDENT_RATIO} \
            || Max children: {stats.MAX_CHILDREN_FOR_PERSON}')

    def end_curses(self):
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()
