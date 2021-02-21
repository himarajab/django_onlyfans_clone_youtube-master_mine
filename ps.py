
from os import error


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

# from collections import Counter
# words = "if there was there was but if \
# there was not there was not".split()
# counts = Counter(words)
# return counts.most_common()

# try:
#   n = int(input('enter number '))
# except ValueError:
#   return 0 

# return sum(range(n + 1))

# x = 1
# if x == '1':
#   print(type(x))



# Two Sum

# from typing import List
# class Solution:
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
#       for i,elem in enumerate(nums):
#         for j,elem2 in enumerate(nums):
#           if elem+elem2 == target and i != j :
#             print(i,j)
#             return i,j
# target= 6
# nums = [3,3]
# my_obj = Solution()
# res = my_obj.twoSum(nums,target)



# list-comprehensions/problem
if __name__ == '__main__':
#     x = int(input())
#     y = int(input())
#     z = int(input())
#     n = int(input())


#     base_list = []
#     for i in range(x+1):
#       for j in range(y+1):
#         for k in range(z+1):
#           if i + j +k != n:
#             base_list.append([i,j,k])
#     print(base_list)


    n = int(input())
    student_marks = {}
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = input()
    my_avg = sum(student_marks[query_name]) / len(student_marks[query_name])
    print(f'{my_avg:.2f}')


