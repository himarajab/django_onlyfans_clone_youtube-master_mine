
def main():
  # animals = [
  #     {'type': 'penguin', 'name': 'Stephanie', 'age': 8},
  #     {'type': 'elephant', 'name': 'Devon', 'age': 3},
  #     {'type': 'puma', 'name': 'Moe', 'age': 5},
  # ]

  # sorted_items = sorted(animals, key=lambda animal: animal['age'])
  # print('in')
  # return sorted_items


#   from collections import defaultdict
#   grades = [
#      ('elliot', 91),
#      ('neelam', 98),
#      ('bianca', 81),
#      ('elliot', 88),
#  ]
#   student_grades = defaultdict(list)
#   for name, grade in grades:
#         student_grades[name].append(grade)

#   return student_grades

  from collections import Counter
  words = "if there was there was but if \
  there was not there was not".split()
  counts = Counter(words)
  return counts.most_common()




    