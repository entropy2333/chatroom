student = {'a': '1001', 'b': '1002', 'c': '1003', 'd': '1004'}
student.pop(list(student.keys())[list(student.values()).index ('1004')])
print(student)