import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time
from scipy.spatial.distance import cosine

##
## Item_basd RS
##
def writeLog(sortlist, up, down, predict_rating):
    # up = 0
    # down = 0
    down_string = ''
    up_string = ''
    for i in range(neighbor_size):
        # down += sortlist[i][1]
        # down_string += str(sortlist[i][1]) + " "
        down_string += "%.3f + " % sortlist[i][1]
        # up += sortlist[i][1] * (ratings_pivotNan[sortlist[i][0]][user_example] - average[sortlist[i][0]])
        # up_string += "%.3f" % sortlist[i][1] + "x(" + "%.3f" % ratings_pivotNan[sortlist[i][0]][user_example] + " - " + "%.3f" % average[sortlist[i][0]] + ") "
        up_string += " %.3f*(%.3f - %.3f) +" % (sortlist[i][1], ratings_pivotNan[sortlist[i][0]][user_example], average[sortlist[i][0]])
    with open('Formula of maximal predict rating.txt', 'a+') as f:
        f.writelines("average: " + str(average[movie_example]) + "\n")
        f.writelines("up_string: " + up_string + "\n")
        f.writelines("down_string: " + down_string + "\n")
        f.writelines("up: " + str(up) + "\n")
        f.writelines("down: " + str(down) + "\n")
        f.writelines("predict rating: " + str(predict_rating) + "\n")


def predictRating(neighbor_size, sortlist, average, ratings_pivotNan):
    print(average)
    print("bone average:", average[movie_example])
    down = 0
    up = 0
    for i in range(neighbor_size):
        down += sortlist[i][1]
        print("current rating:", ratings_pivotNan[sortlist[i][0]][user_example])
        print("average rating:", average[sortlist[i][0]])
        up += sortlist[i][1] * (ratings_pivotNan[sortlist[i][0]][user_example] - average[sortlist[i][0]])
    print("down:", down)
    print("up:", up)
    predict_rating = average[movie_example] + (up / down)
    print("predict rating:", predict_rating)
    print("\n")
    if predict_rating >= 7:
        writeLog(sortlist, up, down, predict_rating)
    return predict_rating

# movies = pd.read_csv('./ez_douban/movies.csv')
movies = pd.read_csv('./data/begin/movies7.csv')
print('number of movies（have title）：%d' % movies[~pd.isnull(movies.title)].shape[0])
print('number of movies（no title）：%d' % movies[pd.isnull(movies.title)].shape[0])
print('number of movies（in total）：%d' % movies.shape[0])
print(movies)

# ratings = pd.read_csv('./ez_douban/testing_ratings.csv')
ratings = pd.read_csv('./data/begin/ratings7.csv')
print('number of users：%d' % ratings.userId.unique().shape[0])
print('number of movies：%d' % ratings.movieId.unique().shape[0])
print('number of ratings：%d' % ratings.shape[0])
print(ratings)


# plt.rc("font", size=15)
# ratings.rating.value_counts(sort=False).plot(kind='bar')
# plt.title('Rating Distribution\n')
# plt.xlabel('Rating')
# plt.ylabel('Count')
# plt.savefig('system1.png', bbox_inches='tight')
# plt.show()

rating_count = pd.DataFrame(ratings.groupby('movieId')['rating'].count())
print(rating_count.sort_values('rating', ascending=False).head(40))
rating_count = pd.DataFrame(ratings.groupby('userId')['rating'].count())
print(rating_count.sort_values('rating', ascending=False).head(40))
print(rating_count.sort_values('rating', ascending=False).mean())


most_rated_movies = pd.DataFrame([15, 470, 90, 39, 53, 45, 5], index=np.arange(7), columns = ['movieId'])
most_rated_movies_summary = pd.merge(most_rated_movies, movies, on='movieId')
print(most_rated_movies_summary)

average_rating = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('movieId')['rating'].count())
print(average_rating.sort_values('ratingCount', ascending=False).head())

# plt.figure(figsize=(10,6))
# plt.scatter(average_rating.rating, average_rating.ratingCount)
# plt.xlabel('average rating')
# plt.ylabel('rating count')
# plt.show()

## who are you
threshold = 0
print("\n" + "If clean the data, it will cause that some users are not available to recommend movies for them")
print("because some users and movies, whose rating count less than the threshold, will be removed from calculation.")
data_clean = int(input("If use want to clean the data, input 1. Otherwise, input 0:"))
if data_clean == 1:
    threshold = int(input("what is the number of threshold:"))

#data cleaning: delete the rating that less than 2 times
if data_clean == 1:
    user_rating_count = ratings['userId'].value_counts()
    ratings = ratings[ratings['userId'].isin(user_rating_count[user_rating_count >= threshold].index)]
    movied_rating_counts = ratings['movieId'].value_counts()
    ratings = ratings[ratings['movieId'].isin(movied_rating_counts[movied_rating_counts >= threshold].index)]
    print(ratings)

print("user list:")
print(ratings['userId'].unique())
user_example = int(input("Please input your user ID:"))
similarity = int(input("If use cosine similarity, input 0; if use pearsonR, input 1:"))
neighbor_size = int(input("Input the neighbor size for calculation:"))


predict_dict = {}
Time_start = time.time()
ratings_pivot = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
print("original pivot table:")
print(ratings_pivot)
rows, columns = ratings_pivot.shape
print(ratings_pivot.shape)
# print("test:", ratings_pivot[840])
print("\n")
# userID = ratings_pivot.index
# movieId = ratings_pivot.columns

unseen_movie = []
##check which movie haven't seen yet, 0 equal to unseen
# print("row:", ratings_pivot.loc[user_example], "\n")
# ## find unseen movie id without data cleaning
# id = 0
# for movie in ratings_pivot.loc[user_example]:
#     # id += 1
#     if movie == 0:
#         # print(id)
#         unseen_movie.append(id)
#     id += 1
# # unseen_movie.remove(columns)
# print("unseen movie id:", unseen_movie, "\n")

## find unseen movie id with data cleaning
# id = 0
# print(ratings_pivot.columns.values)
# print(ratings_pivot[5][user_example])
for movieid in ratings_pivot.columns.values:
    # id += 1
    if ratings_pivot[movieid][user_example] == 0:
        # print(id)
        unseen_movie.append(movieid)
# unseen_movie.remove(columns)
print("unseen movie id:", unseen_movie, "\n")



for movie_example in unseen_movie:
    ## if you choose user 2, then all of the NaN value will set to default value 0 except user 2

    # if similarity == 0:
    #     ratings_pivot = ratings_pivot.fillna(0)   ##no cosine similarity

    ratings_pivotNan = ratings_pivot

    # if similarity == 0:
    #     ratings_pivotNan[movie_example][user_example] = np.nan    ##no cosine similarity

    print("predict movie:", movie_example, "and add a NaN to it for calculation", "\n")
    # print("ratings_pivotNan:")
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
        # print("cancel all the NaN:")
        # print(ratings_pivot)
        # print(bones_ratings_for_pearson)
        similar_to_bones = ratings_pivot.corrwith(bones_ratings_for_pearson, method='pearson')
        pearson_dict = {}
        for key in similar_to_bones.index:
            if key == movie_example:
                continue
            pearson_dict[key] = similar_to_bones[key]
        print("pearson correlation:")
        print(pearson_dict)
        sortlist = sorted(pearson_dict.items(), key=lambda item:item[1], reverse=True)
        print(sortlist)
        print("\n")


    ## cosine similarity
    if similarity == 0:
        bones_ratings = ratings_pivotNan[movie_example].drop([user_example])
        print("bones_ratings:")
        print(bones_ratings)
        print("\n")
        ## remove the row that have Nan value
        rating_remove_column = ratings_pivotNan.drop([user_example])
        print("rating_remove_column:")
        print(rating_remove_column)
        print("\n")
        dict = {}
        userlist_length, movielist_length = ratings_pivotNan.shape
        # for i in range(0, movielist_length):    ##change 1 to 0, movielist_length + 1 to movielist_length
        #     if i == movie_example:
        #         continue
        #     # print(rating_remove_column[i])
        #     dict[i] = 1 - cosine(rating_remove_column[i], bones_ratings)

        for movieid in ratings_pivot.columns.values:
            if movieid == movie_example:
                continue
            dict[movieid] = 1 - cosine(rating_remove_column[movieid], bones_ratings)

        for key in dict.keys():
            if np.isnan(dict[key]):
                # print("is Nan")
                dict[key] = 0
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
    print("predict_dict:", predict_dict)




recommend_movie_id_list = []
recommend_sort_list = sorted(predict_dict.items(), key=lambda item:item[1], reverse=True)
print(recommend_sort_list, "\n")

recommend_movie_predict_rating_list = sorted(predict_dict.values(), reverse=True)
print("recommend_movie_predict_rating_list:")
print(recommend_movie_predict_rating_list)
print(len(recommend_movie_predict_rating_list), "\n")

for list in recommend_sort_list:
    recommend_movie_id_list.append(list[0])
print("recommand_movie_id_list:", len(recommend_movie_id_list), "\n")
recommend_movies = pd.DataFrame(recommend_movie_id_list, index=np.arange(len(recommend_movie_id_list)), columns = ['movieId'])
recommend_movies_summary = pd.merge(recommend_movies, movies, on='movieId')
print("recommend_movies_summary:")
print(len(recommend_movies_summary), "\n")
recommend_movies_summary['predict_ratings'] = recommend_movie_predict_rating_list
print("recommende to user", user_example)
print(recommend_movies_summary)
Time_end = time.time()
print("time cost:", Time_end - Time_start)
recommend_movies_summary.to_csv('./data/begin/recommendation.csv')



