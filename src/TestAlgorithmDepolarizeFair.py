from RecSys import RecSys
from AlgorithmUserFairness import Polarization, IndividualLossVariance, RMSE
from AlgorithmDepolarizeFair import AlgorithmDepolarize
import pandas as pd

def print_results(dataset, algorithm, alpha, h, n_users, n_items, Rpol, Rindv, result, original=False):

    if original == True:
        h = 0

    print(f'Dataset: {dataset}; Algorithm: {algorithm}; alpha: {alpha}; h: {h}; n_users: {n_users}; n_items: {n_items}')
    print(f'Polarization (Rpol): {Rpol:.9f}')
    print(f'Individual Loss Variance (Rindv): {Rindv:.9f}')
    print(f'Root Mean Squared Error (RMSE): {result:.9f}')

    # Write the results to the file _results.txt
    with open('_results.txt', 'a') as file:
        file.write(f'\nDataset: {dataset}; Algorithm: {algorithm}; alpha: {alpha}; h: {h}; n_users: {n_users}; n_items: {n_items}\n')
        file.write(f'Polarization (Rpol): {str(Rpol).replace(".", ",")}\n')
        file.write(f'Individual Loss Variance (Rindv): {str(Rindv).replace(".", ",")}\n')
        file.write(f'Root Mean Squared Error (RMSE): {str(result).replace(".", ",")}\n')

    experiment_results.append({
        'Dataset': dataset, 
        'Algorithm': algorithm, 
        'alpha': alpha,
        'h': h, 
        'n_users': n_users, 
        'n_items': n_items, 
        'Polarization (Rpol)': str(Rpol).replace(".", ","), 
        'Individual Loss Variance (Rindv)': str(Rindv).replace(".", ","), 
        'Root Mean Squared Error (RMSE)': str(result).replace(".", ",")
    })


def save_matrices(X, X_est, X_pi, dataset, algorithm):
    print("\n\nX")
    print(X)
    print("\n\nX_est")
    print(X_est)
    print("\n\nX_pi")
    print(X_pi)
    X.to_excel(f'X_{dataset}_{algorithm}.xlsx', index=True)
    X_est.to_excel(f'Xest_{dataset}_{algorithm}.xlsx', index=True)
    X_pi.to_excel(f'XestPi_{dataset}_{algorithm}.xlsx', index=True)    


experiment_results = []

# user and item filtering
n_users=  1000
n_items= 1000
top_users = True # True: to use users with more ratings; False: otherwise
top_items = True # True: to use MovieLens with more ratings; False: otherwise

# datasets
# 'MovieLens-1M'  reading data from 3883 movies and 6040 users
# 'Goodbooks-10k' reading data from 10000 GoodBooks and 53424 users
datasets = ['MovieLens-1M', 'Goodbooks-10k']

# recommendation algorithm
algorithms = ['RecSysALS'] # Alternating Least Squares (ALS) for Collaborative Filtering

# estimated number of matrices (h)
hs = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40]

# Adjustment factor for the fraction of data deviation towards the mean (α)
alphas = [0.2, 0.4, 0.6, 0.8]


for dataset in datasets:

    Data_path = "Data/"+ dataset    

    for alpha in alphas:

        for algorithm in algorithms:
            first_original = True

            for h in hs:
                recsys = RecSys(n_users, n_items, top_users, top_items)

                X, users_info, items_info = recsys.read_dataset(n_users, n_items, top_users, top_items, data_dir = Data_path) # returns matrix of ratings with n_users rows and n_items columns
                omega = ~X.isnull() # matrix X with True in cells with evaluations and False in cells not rated

                X_est = recsys.compute_X_est(X, algorithm) # RecSysALS or RecSysKNN or RecSysNMF or RecSysExampleAntidoteData20Items
                X_est_0 = X_est.copy()
                print("\n\n------------ SOCIAL OBJECTIVE FUNCTIONS [before the impartiality algorithm] ------------")

                # To capture polarization, we seek to measure the extent to which the user ratings disagree
                polarization = Polarization()
                Rpol = polarization.evaluate(X_est)

                # Individual fairness. For each user i, the loss of user i, is  the mean squared estimation error over known ratings of user i
                ilv = IndividualLossVariance(X, omega, 0) #axis = 1 (0 rows e 1 columns) 0 para itens e 1 para usuários
                Rindv = ilv.evaluate(X_est)

                rmse = RMSE(X, omega)
                result = rmse.evaluate(X_est)

                list_users = X_est.index.tolist()
                list_items = X_est.columns.tolist()

                if first_original:
                    first_original = False
                    print_results(dataset, algorithm, alpha, h, n_users, n_items, Rpol, Rindv, result, original=True)

                ##############################################################################################################################
                algorithmDepolarize = AlgorithmDepolarize(X, omega, 0)
                list_X_est = algorithmDepolarize.evaluate(X_est, alpha, h) # calculates a list of h estimated matrices

                print("\n--------------------------------- optimization result ----------------------------------")

                list_losses = []
                for X_est in list_X_est:
                    losses = ilv.get_losses(X_est)
                    list_losses.append(losses)
                # print("list_losses")
                # print(list_losses)

                list_polarizations = []
                for X_est in list_X_est:
                    polarizations = polarization.get_polarizations(X_est)
                    list_polarizations.append(polarizations)
                # print("list_polarizations")
                # print(list_polarizations)

                ZIL = AlgorithmDepolarize.losses_to_ZIL(list_losses, n_items) # Matriz Z para as perdas individuais dos itens
                ZIP = AlgorithmDepolarize.polarizations_to_ZIP(list_polarizations, n_items) # Matriz Z para as polarizações individuais dos itens

                # Calculate the recommendation matrix optimized by Simulated Annealing
                X_pi = AlgorithmDepolarize.make_matrix_X_pi_annealing(list_X_est, ZIL, ZIP)
                X_pi.columns = X.columns # Rename the columns of X_pi to match those of X
                X_pi = X_pi.loc[X.index] # Align the indices of X_pi with those of X

                Rpol = polarization.evaluate(X_pi)
                Rindv = ilv.evaluate(X_pi)
                result = rmse.evaluate(X_pi)

                print("\n\n------------ SOCIAL OBJECTIVE FUNCTIONS [after the impartiality algorithm] ------------")
                print_results(dataset, algorithm, alpha, h, n_users, n_items, Rpol, Rindv, result, original=False)
                if h == hs[-1]: # Save results from the last execution
                    print(f'h: {h}')
                    save_matrices(X, X_est_0, X_pi, dataset, algorithm)


df_experiment_results = pd.DataFrame(experiment_results)
df_experiment_results.to_csv('_results.csv', sep=';', index=False)

print('The results of the experiments were successfully saved in "_results.csv".".')