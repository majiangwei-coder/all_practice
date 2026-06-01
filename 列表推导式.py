from pyreadline3.console import event

print(list(set(['b', 'c', 'd', 'e', 'a', 'a'])))

print(list(dict.fromkeys(['b', 'c', 'd', 'e', 'a', 'a'])))


even_numbers = [x for x in range(101) if x % 2 == 0]
print(even_numbers)

print([x for x in range(101) if x % 2 == 0])
