import random

block_array = []

for i in range(30):
    row = []
    for j in range(30):
        value = random.randint(0, 1)
        if value == 1:
            row.append('F')
        else:
            row.append('0')
    block_array.append(row)

for row in block_array:
    print(" ".join(row))