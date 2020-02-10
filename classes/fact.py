import csv
import os.path

class Fact:
  def __init__(self, id, fact):
    self.id = id
    self.fact = fact

  @classmethod
  def all_facts(self):
    facts = []
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../facts.csv")
    with open(path) as csvfile:
      csv_reader = csv.DictReader(csvfile)
      for row in csv_reader:
        dict_row = dict(row)
        facts.append(Fact(dict_row['id'], dict_row['fact']))
    return facts
