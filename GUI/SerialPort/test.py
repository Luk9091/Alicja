import matplotlib.pyplot as plt
import sys

path = sys.argv[1]
data = []
with open(path, "r") as file:
    for line in file:
        line = line.strip(",\n")
        data.extend(map(int, line.strip().split(',')))


differences = [abs(data[i] - data[i-1]) for i in range(1, len(data))]

print(f"Count: {len(data)}")
print(f"Maximum difference: {max(differences)}")
plt.plot(data, drawstyle="steps-post")
# plt.plot(differences, drawstyle="steps-post")
plt.show()