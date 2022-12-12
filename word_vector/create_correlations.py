import numpy as np

with open("small.txt") as f:
    lines = f.read().split("\n")

words = []
vectors = []
for line in lines:
    parts = line.split()
    word, *vector = parts
    words.append(word)
    vector = [float(x) for x in vector]
    vectors.append(vector)

vectors = np.array(vectors)
norms = (vectors ** 2).sum(axis=1, keepdims=True) ** 0.5
vectors /= norms
dots = vectors @ vectors.T
dots[range(len(dots)), range(len(dots))] = np.percentile(dots, 50)
print(dots)

with open("words.txt", 'w') as f:
    f.write("\n".join(words))

with open("correlations.npy", 'wb') as f:
    np.save(f, dots)