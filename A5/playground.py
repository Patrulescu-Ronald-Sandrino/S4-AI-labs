
a = {2: -1, 3: 4}

# a = {2: max(a[2], -2), 3: 4}

a = {x: -1 for x in range(5*3)}
print(a)
a = {x + y: max(a[x + y], x + y) for x in range(9) for y in range(5)}
a = {x + y: max(a[x + y], x, y) for x in range(9) for y in range(5)}
a = {x + y: max(x, y) for x in range(9) for y in range(5)}
print(a)
a = {x + y: max(a[x + y], x, y) for x in range(5) for y in range(9)}
a = {x + y: max(x, y) for x in range(5) for y in range(9)}
# a = {x + y: max(x, y) for x in range(5)} for y in range(9) # doesn't work: syntax error
print(a)
# print({key: value for key, value in range(10), range(5)})
print()
print({key + value: value for key, value in ((x, y) for x in range(5) for y in range(3))})
print({key + value: key for key, value in ((x, y) for x in range(3) for y in range(5))})
x = [(key, value) for key, value in ((x, y) for x in range(3) for y in range(5))]
# x = [(key, value) for key, value in ((range(3), range(5)))] # doesn't work: syntax error
print(len(x), x)