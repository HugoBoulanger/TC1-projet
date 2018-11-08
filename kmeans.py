from sklearn.cluster import MiniBatchKMeans
import numpy as np
import time
import json

f = open('vectorized.txt', 'r')
vec = json.load(f)
f.close()

vec = np.array(vec)
vec = np.reshape(vec, (vec.shape[0], 52))
print(vec[:20])


t = time.time()
kmeans = MiniBatchKMeans(n_clusters=10000, verbose=True, max_iter=1, batch_size=10000).fit_predict(vec)
print(time.time() - t)
f = open('cl.txt', 'w')
l = []
for i in range(kmeans.shape[0]):
    l.append(int(kmeans[i]))
json.dump(l, f)
f.close()
