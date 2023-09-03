import numpy as np

s1 = 'It was a good time'
s2 = 'It was a worst time'
s3 = [s1, s2]
words = list(set((s1+' '+s2).split()))
print(words)

results = np.zeros((len(s3), len(words))) 

for i, sequence in enumerate(s3): 
    for j in sequence.split():
        results[i, words.index(j)] = 1.

print(results)