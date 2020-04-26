from interface import Interface
import threading
import time

interface_lock = threading.Lock()
alive = 1
interface = Interface()


class PersonThread(threading.Thread):

    def __init__(self, person, person_number):
        threading.Thread.__init__(self)
        self.person = person
        self.person_number = person_number

    def run(self):
        global alive
        alive += 1

        while not interface.is_curses_initialized:
            time.sleep(0.1)

        while self.person.alive:
            interface_lock.acquire()
            interface.print_person(self.person_number, self.person)

            interface_lock.release()

            time.sleep(1)

            self.person.increase_age()

            if self.person.age >= self.person.life_expectancy:
                self.person.kill()

        interface_lock.acquire()
        interface.print_person_death(self.person_number, self.person)
        interface_lock.release()
        alive -= 1

        time.sleep(0.1)


class InterfaceThread(threading.Thread):

    def run(self):
        interface_lock.acquire()

        interface.init_interface()
        interface.print_info()

        interface_lock.release()

        while alive > 0:
            interface_lock.acquire()
            interface.refresh_display()
            interface_lock.release()

            time.sleep(1)

        interface_lock.acquire()
        interface.end_curses()
        interface_lock.release()
        time.sleep(0.1)


interface_lock.acquire()
ui = InterfaceThread()
ui.start()
