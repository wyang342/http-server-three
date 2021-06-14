import os
import csv


class Fact:
    facts = []

    def __init__(self, id, fact) -> None:
        self.id = id
        self.fact = fact

    @classmethod
    def all_facts(cls):
        dir_path = os.getcwd()
        path = os.path.join(dir_path, 'facts.csv')

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                cls.facts.append(Fact(**line))

        return cls.facts
