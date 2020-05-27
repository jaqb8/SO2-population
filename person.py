import random
import stats


class Person:

    def __init__(self):
        self.alive = True
        self.gender = random.choice(['Male', 'Female'])
        self.life_expectancy = random.randrange(
            stats.AGE_LIMIT / 2, stats.AGE_LIMIT)

    def init_random_person(self):
        self.age = random.randrange(1, stats.AGE_LIMIT / 2)
        self.children = random.randrange(0, stats.MAX_CHILDREN_FOR_PERSON)

    def init_child(self):
        self.age = 1
        self.children = 0

    def increase_age(self):
        self.age += 1

    def kill(self):
        self.alive = False

    def can_have_child(self):
        if not self.alive:
            return False

        if self.children >= stats.MAX_CHILDREN_FOR_PERSON:
            return False

        if self.age >= stats.BIRTH_MAX_AGE:
            return False

        if self.age <= stats.BIRTH_MIN_AGE:
            return False

        return True
