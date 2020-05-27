from interface import Interface
from person import Person
import threading
import time
import stats

interface_lock = threading.Lock()
alive = 0
interface = Interface()
interface.init_interface()
population = list()
threads = list()


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


def main():
    for _ in range(stats.STARTING_POPULATION_SIZE):
        person = Person()
        person.init_random_person()
        population.append(person)

    for i in range(stats.STARTING_POPULATION_SIZE):
        t = threading.Thread(target=person_thread, args=[population[i], i])
        t.start()
        threads.append(t)

    interface_t = threading.Thread(target=interface_thread)
    interface_t.start()
    interface_t.join()

    for thread in threads:
        thread.join()


main()
