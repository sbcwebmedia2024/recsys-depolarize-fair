import pandas as pd
import numpy as np

import RecSysALS
import RecSysKNN
import RecSysNMF
import RecSysSGD
import RecSysSVD
import RecSysNCF


class RecSys():
        
    def __init__(self, n_users, n_items, top_users, top_items, l=5, theta=3, k=3):
        self.n_users = n_users
        self.n_items = n_items
        self.top_users = top_users
        self.top_items = top_items
        self.l = l
        self.theta = theta
        self.k = k

    ###################################################################################################################
    def read_dataset(self, n_users, n_items, top_users, top_items, data_dir):
        parts = data_dir.split("Data/")
        path = parts[0]  # Contém "Data/"
        dataset_name = parts[1]  # Contém o nome do dataset
        if dataset_name == 'MovieLens-1M':
            return self.read_movielens_1M(n_users, n_items, top_users, top_items, data_dir)
        elif dataset_name == 'Goodbooks-10k':
            print("read_dataset :: Goodbooks-10k")
            return self.read_goodbooks(n_users, n_items, top_users, top_items, data_dir)
        elif dataset_name == 'Songs':
            return self.read_songs(n_users, n_items, top_users, top_items, data_dir)
        elif dataset_name == 'Eletronics':
            return self.read_eletronics(n_users, n_items, top_users, top_items, data_dir)
        else:
            return self.read_movielens_1M(n_users, n_items, top_users, top_items, data_dir)
    

    def read_movielens_1M(self, n_users, n_items, top_users, top_items, data_dir):
        # get ratings
        df = pd.read_table('{}/ratings.dat'.format(data_dir),names=['UserID','MovieID','Rating','Timestamp'], sep='::', engine='python')

        # create a dataframe with movie IDs on the rows and user IDs on the columns
        ratings = df.pivot(index='MovieID', columns='UserID', values='Rating')

        users_info = pd.read_table('{}/users.dat'.format(data_dir), names=['UserID','Gender','Age','Occupation','Zip-code'], sep='::', engine='python', encoding = "ISO-8859-1")
        users_info = users_info.rename(index=users_info['UserID'])[['Gender','Age','Occupation','Zip-code']]

        items_info = pd.read_table('{}/movies.dat'.format(data_dir), names=['MovieID', 'Title', 'Genres'], sep='::', engine='python', encoding = "ISO-8859-1")
        
        movieSeries = pd.Series(list(items_info['MovieID']), index=items_info['MovieID'])
        ratings = ratings.rename(index=movieSeries)
        
        if top_items and top_users:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]

            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just u
        elif top_items:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]
        elif top_users:
            # select the top n_users with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just updated the index)
        else:
            # select the first n_users from the matrix
            cols = ratings.columns[0:n_users]
            ratings = ratings[cols] # matrix [n_movies rows , n_users columns]; before [n_movies rows , original columns]

        ratings = ratings.T # transposed: matrix [n_users rows x n_movies columns];
        
        # Modificações
        ratings = ratings.dropna(how='all')
        ratings = ratings.dropna(axis=1, how='all')
        ratings = ratings.reset_index(drop=True)
        ratings.columns = range(ratings.shape[1])

        return ratings, users_info, items_info


    ###################################################################################################################
    # function to read the data
    def read_movielens_small(self, n_users, n_items, top_users, top_items, data_dir):
        # get ratings
        df = pd.read_table('{}/ratings.dat'.format(data_dir),names=['UserID','MovieID','Rating','Timestamp'], sep='::', engine='python')

        # create a dataframe with movie IDs on the rows and user IDs on the columns
        ratings = df.pivot(index='MovieID', columns='UserID', values='Rating')
        
        items_info = pd.read_table('{}/movies.dat'.format(data_dir), names=['MovieID', 'Title', 'Genres', 'Price'], sep='::', engine='python')
        
        # put movie titles as index on rows
        movieSeries = pd.Series(list(items_info['Title']), index=items_info['MovieID'])
        ratings = ratings.rename(index=movieSeries)

        users_info = pd.read_table('{}/users.dat'.format(data_dir), names=['UserID','Gender','Age','NR','SPI', 'MA', 'MR'], sep='::', engine='python')
        users_info = users_info.rename(index=users_info['UserID'])[['Gender','Age','NR','SPI', 'MA', 'MR']]

        if top_items:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]
        
        if top_users:
            # select the top n_users with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just updated the index)
        else:
            # select the first n_users from the matrix
            cols = ratings.columns[0:n_users]
            ratings = ratings[cols] # matrix [n_movies rows , n_users columns]; before [n_movies rows , original columns]

        ratings = ratings.T # transposed: matrix [n_users rows x n_movies columns];

        return ratings, users_info, items_info
    

    ###################################################################################################################
    # function to read the data
    def read_books(self, n_users, n_items, top_users, top_items, data_dir):
        # get ratings
        df = pd.read_csv('{}/ratings.csv'.format(data_dir), sep=';')

        # create a dataframe with item IDs on the rows and user IDs on the columns
        ratings = df.pivot(index='BookID', columns='UserID', values='Rating')
        
        users_info = pd.read_csv('{}/users.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
        
        items_info = pd.read_csv('{}/books.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
                            
        users_info = users_info.rename(index=users_info['UserID'])[['Location','Age']]

        # add number of ratings in users_info
        num_ratings = (~ratings.isnull()).sum(axis=0)
        users_info['NR'] = num_ratings
        
        # put movie titles as index on rows
        #movieSeries = pd.Series(list(movies['Title']), index=movies['MovieID'])
        #ratings = ratings.rename(index=movieSeries)

        if top_items:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]
        
        if top_users:
            # select the top n_users with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just updated the index)
        else:
            # select the first n_users from the matrix
            cols = ratings.columns[0:n_users]
            ratings = ratings[cols] # matrix [n_movies rows , n_users columns]; before [n_movies rows , original columns]

        ratings = ratings.T # transposed: matrix [n_users rows x n_movies columns];

        return ratings, users_info, items_info

    
    ###################################################################################################################
    # function to read the data
    def read_songs(self, n_users, n_items, top_users, top_items, data_dir):
        
        # get ratings
        df = pd.read_csv('{}/ratings.csv'.format(data_dir), sep=';')

        # create a dataframe with item IDs on the rows and user IDs on the columns
        ratings = df.pivot(index='SongID', columns='UserID', values='Rating')
        ratings = ratings.dropna(how='all')
        ratings = ratings.dropna(how='all', axis=1)
        
        users_info = pd.read_csv('{}/users.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
        
        items_info = pd.read_csv('{}/songs.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
                            
        users_info = users_info.rename(index=users_info['UserID'])

        # put movie titles as index on rows
        #movieSeries = pd.Series(list(movies['Title']), index=movies['MovieID'])
        #ratings = ratings.rename(index=movieSeries)

        if top_items and top_users:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]

            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just u
        elif top_items:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]
        elif top_users:
            # select the top n_users with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just updated the index)
        else:
            # select the first n_users from the matrix
            cols = ratings.columns[0:n_users]
            ratings = ratings[cols] # matrix [n_movies rows , n_users columns]; before [n_movies rows , original columns]

        ratings = ratings.T # transposed: matrix [n_users rows x n_movies columns];
        return ratings, users_info, items_info
    

    ###################################################################################################################
    # function to read the data
    def read_goodbooks(self, n_users, n_items, top_users, top_items, data_dir):
        
        # get ratings
        df = pd.read_csv('{}/ratings.csv'.format(data_dir), sep=';')

        # create a dataframe with item IDs on the rows and user IDs on the columns
        ratings = df.pivot(index='BookID', columns='UserID', values='Rating')
        
        users_info = pd.read_csv('{}/users.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
        
        items_info = pd.read_csv('{}/books.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
                            
        users_info = users_info.rename(index=users_info['UserID'])

        # put movie titles as index on rows
        #movieSeries = pd.Series(list(movies['Title']), index=movies['MovieID'])
        #ratings = ratings.rename(index=movieSeries)

        if top_items and top_users:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]

            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just u
        elif top_items:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]
        elif top_users:
            # select the top n_users with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just updated the index)
        else:
            # select the first n_users from the matrix
            cols = ratings.columns[0:n_users]
            ratings = ratings[cols] # matrix [n_movies rows , n_users columns]; before [n_movies rows , original columns]

        ratings = ratings.T # transposed: matrix [n_users rows x n_movies columns];
        
        # Modificações
        ratings = ratings.dropna(how='all')
        ratings = ratings.dropna(axis=1, how='all')
        ratings = ratings.reset_index(drop=True)
        ratings.columns = range(ratings.shape[1])

        return ratings, users_info, items_info


    ###################################################################################################################
    def read_eletronics(self, n_users, n_items, top_users, top_items, data_dir):
        
        # get ratings
        df = pd.read_csv('{}/ratings.csv'.format(data_dir), sep=';')

        # create a dataframe with item IDs on the rows and user IDs on the columns
        ratings = df.pivot(index='ProductID', columns='UserID', values='Rating')
        
        # users_info = pd.read_csv('{}/users.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
        
        # items_info = pd.read_csv('{}/books.csv'.format(data_dir), sep=';', encoding = "ISO-8859-1")
                            
        # users_info = users_info.rename(index=users_info['UserID'])

        # put movie titles as index on rows
        #movieSeries = pd.Series(list(movies['Title']), index=movies['MovieID'])
        #ratings = ratings.rename(index=movieSeries)

        if top_items and top_users:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]

            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just u
        elif top_items:
            # select the top n_movies with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=1) # quantitative ratings for each movie: Movie 1: 4, Movie 2: 5, Movie 3: 2 ...
            rows = num_ratings.nlargest(n_items) # quantitative ratings for each movie (n_movies) sorted: Movie 7: 6, Movie 2: 5, Movie 1: 4 ...
            ratings = ratings.loc[rows.index] # matrix[n_movies rows , original columns]; before [original rows x original columns]
        elif top_users:
            # select the top n_users with the highest number of ratings
            num_ratings = (~ratings.isnull()).sum(axis=0) # quantitative ratings made by each user: User 1: 5, User 2: 5, User 3: 5, ...
            cols = num_ratings.nlargest(n_users) # quantitative evaluations by each user (n_users) sorted: User 1: 5, User 2: 5, User 3: 5, ...
            ratings = ratings[cols.index] # matrix [n_movies rows , original columns]; before [n_movies rows , original columns] (just updated the index)
        else:
            # select the first n_users from the matrix
            cols = ratings.columns[0:n_users]
            ratings = ratings[cols] # matrix [n_movies rows , n_users columns]; before [n_movies rows , original columns]

        ratings = ratings.T # transposed: matrix [n_users rows x n_movies columns];

        return ratings, [], []



    ###################################################################################################################
    # compute_X_est: 
    def  compute_X_est(self, X, algorithm='RecSysALS', data_dir="Data/MovieLens-Small"):
        if(algorithm == 'RecSysALS'):
            # factorization parameters
            rank = 1 # before 20
            lambda_ = 1 # before 20 - ridge regularizer parameter
            # initiate a recommender system of type ALS (Alternating Least Squares)
            RS = RecSysALS.als_RecSysALS(rank,lambda_)
            X_est, error = RS.fit_model(X)
        elif(algorithm == 'RecSysKNN'):
            #RS = RecSysKNN.RecSysKNN(k=5, ratings=X, user_based=True)
            RS = RecSysKNN.RecSysKNN(k=5, ratings=X)
            X_est = RS.fit_model()
        elif(algorithm == 'RecSysNMF'):
            RS = RecSysNMF.RecSysNMF(n_components=5, ratings=X)
            X_est = RS.fit_model()
        elif(algorithm == 'RecSysSGD'):
            RS = RecSysSGD.RecSysSGD(n_factors=10, learning_rate=0.01, n_epochs=20, lambda_=0.1, ratings=X)
            X_est = RS.fit_model()
        elif(algorithm == 'RecSysSVD'):
            RS = RecSysSVD.RecSysSVD(n_factors=50, ratings=X)
            X_est, error = RS.fit_model()
        elif(algorithm == 'RecSysNCF'):
            RS = RecSysNCF.RecSysNCF(n_users=self.n_users, n_items=self.n_items, n_factors=20, ratings=X)
            X_est, error = RS.fit_model()
        else:
            RecSysNMF
        return X_est  
        

#######################################################################################################################

