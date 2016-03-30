# first two digits are 18, last four digits are random
# student id numbers are unique
num_students = 2000
m = 6
from collections import defaultdict
student_id_str_to_count_dict = defaultdict(lambda: 0)
import random
while len(student_id_str_to_count_dict) < num_students:
  student_id_str = ""
  for i in xrange(m):
    digit = random.randint(0, 9)
    digit_str = str(digit)
    student_id_str += digit_str
  if student_id_str in student_id_str_to_count_dict:
    continue
  else:
    student_id_str_to_count_dict[student_id_str] += 1
student_id_str_list = student_id_str_to_count_dict.keys()
sorted_student_id_str_list = sorted(student_id_str_list, key = lambda x: int(x))
print m, num_students
for student_id_str in sorted_student_id_str_list:
  print student_id_str
