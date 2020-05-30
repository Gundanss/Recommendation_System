import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

movies = pd.read_csv('./data/output7.csv')
print(movies)
rows, column = movies.shape

# print(range(rows))
# print(movies['userId'][0])
# user = movies['userId'][0]
# print(user)
# movies['userId'][0] = 0
# print(movies)
print(movies["userId"].unique())
id = 0

for userId in movies["userId"].unique():
    for j in range(rows):
        if movies["userId"][j] == userId:
            movies["userId"][j] = id
    id += 1

print(movies)

id = 0
for movieId in movies["movieId"].unique():
    for j in range(rows):
        if movies["movieId"][j] == movieId:
            movies["movieId"][j] = id
    id += 1

print(movies)
movies.to_csv('./data/output7_update.csv')



