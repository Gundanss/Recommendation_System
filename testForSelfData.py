import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine


def predictRating(neighbor_size, sortlist, average, ratings_pivotNan):
    print("bone average:", average[movie_example])
    down = 0
    up = 0
    for i in range(neighbor_size):
        down += sortlist[i][1]
        print(ratings_pivotNan[sortlist[i][0]][user_example])
        print(average[sortlist[i][0]])
        up += sortlist[i][1] * (ratings_pivotNan[sortlist[i][0]][user_example] - average[sortlist[i][0]])
    print("down:", down)
    print("up:", up)
    predict_rating = average[movie_example] + (up / down)
    print("predict rating:", predict_rating)
    print("\n")
    return predict_rating

movies = pd.read_csv('./ez_douban/movies.csv')
# print('电影数目（有名称）：%d' % movies[~pd.isnull(movies.title)].shape[0])
# print('电影数目（没有名称）：%d' % movies[pd.isnull(movies.title)].shape[0])
# print('电影数目（总计）：%d' % movies.shape[0])
print(movies)

ratings = pd.read_csv('./ez_douban/testing_ratings.csv')
# print('用户数据：%d' % ratings.userId.unique().shape[0])
# print('电影数据：%d' % ratings.movieId.unique().shape[0])
# print('评分数目：%d' % ratings.shape[0])
print(ratings)

## who are you
user_example = int(input("From " + str(1) + " to " + str(ratings.userId.unique().shape[0]) + ". Please input your user ID:"))
similarity = int(input("If use cosine similarity, input 0; if use pearsonR, input 1:"))
neighbor_size = 2
predict_dict = {}
ratings_pivot = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
print("original pivot table:")
print(ratings_pivot)
print(ratings_pivot.shape)
print("\n")
# userID = ratings_pivot.index
# movieId = ratings_pivot.columns

unseen_movie = []
##check which movie haven't seen yet, 0 equal to unseen
# print("row:", ratings_pivot.loc[user_example], "\n")
id = 0
for movie in ratings_pivot.loc[user_example]:
    id += 1
    if movie == 0:
        print(id)
        unseen_movie.append(id)
print("unseen movie id:", unseen_movie, "\n")

for movie_example in unseen_movie:
    ## if you choose user 2, then all of the NaN value will set to default value 0 except user 2

    # ratings_pivot = ratings_pivot.fillna(0)

    ratings_pivotNan = ratings_pivot

    # ratings_pivotNan[movie_example][user_example] = np.nan

    print("predict movie:", movie_example, "and add a NaN to it for calculation")
    # print(ratings_pivotNan)
    print("\n")

    # 有NaN的表只用来计算average
    ## step1: calculate average ratings of all movies
    average = ratings_pivotNan.mean()
    # print("average:")
    # print(average)
    # print("\n")


    ##calculate step2: calculate the similarity of bones and other columns
    if similarity == 1:
        ## pearson correlation
        ratings_pivot = ratings_pivot.fillna(0)
        bones_ratings_for_pearson = ratings_pivot[movie_example]
        print("cancel all the NaN:")
        # print(ratings_pivot)
        # print(bones_ratings_for_pearson)
        similar_to_bones = ratings_pivot.corrwith(bones_ratings_for_pearson, method='pearson')
        pearson_dict = {}
        for key in similar_to_bones.index:
            if key == movie_example:
                continue
            pearson_dict[key] = similar_to_bones[key]
        print("pearson correlation:")
        # print(pearson_dict)
        sortlist = sorted(pearson_dict.items(), key=lambda item:item[1], reverse=True)
        print(sortlist)
        print("\n")


    # ## cosine similarity
    if similarity == 0:
        bones_ratings = ratings_pivotNan[movie_example].drop([user_example])
        print("bones_ratings:")
        # print(bones_ratings)
        # print("\n")
        ## remove the row that have Nan value
        rating_remove_column = ratings_pivotNan.drop([user_example])
        print("rating_remove_column:")
        # print(rating_remove_column)
        # print("\n")
        dict = {}
        userlist_length, movielist_length = ratings_pivotNan.shape
        for i in range(1, movielist_length + 1):
            if i == movie_example:
                continue
            dict[i] = 1 - cosine(rating_remove_column[i], bones_ratings)
        print("similarity:", dict)
        ##sort the similarity
        # sort_list = sorted(dict.values(), reverse=True)
        # print(sort_list[0:neighbor_size])
        # print(dict[sort_list[1]])
        sortlist = sorted(dict.items(), key=lambda item:item[1], reverse=True)
        print(sortlist)
        print("\n")

    ##step3: predict the user's ratings of unseen movie
    # print(predictRating(neighbor_size, sortlist, average, ratings_pivotNan))
    predict_dict[movie_example] = predictRating(neighbor_size, sortlist, average, ratings_pivotNan)
    print(predict_dict)




recommend_movie_id_list = []
recommend_sort_list = sorted(predict_dict.items(), key=lambda item:item[1], reverse=True)
recommend_movie_predict_rating_list = sorted(predict_dict.values(), reverse=True)
for list in recommend_sort_list:
    recommend_movie_id_list.append(list[0])
print("recommand_movie_id_list", recommend_movie_id_list)
recommend_movies = pd.DataFrame(recommend_movie_id_list, index=np.arange(len(recommend_movie_id_list)), columns = ['movieId'])
recommend_movies_summary = pd.merge(recommend_movies, movies, on='movieId')
recommend_movies_summary['predict_ratings'] = recommend_movie_predict_rating_list
print(recommend_movies_summary)




