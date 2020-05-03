from interface import Interface
from person import Person
import threading
import time

interface_lock = threading.Lock()
alive = 1
interface = Interface()
interface.init_interface()


def person_thread(person, person_number):
    global alive
    alive += 1

    while not interface.is_curses_initialized:
        time.sleep(.1)

    while person.alive:
        with interface_lock:
            interface.print_person(person_number, person)

        time.sleep(1)
        person.increase_age()

        if person.age >= person.life_expectancy:
            person.kill()

    with interface_lock:
        interface.print_person_death(person_number, person)

    alive -= 1
    time.sleep(.1)


def interface_thread():
    with interface_lock:
        interface.init_interface()
        interface.print_info()

    global alive
    while alive > 0:
        with interface_lock:
            interface.refresh_display()
        time.sleep(1)

    with interface_lock:
        interface.end_curses()

    time.sleep(.1)
