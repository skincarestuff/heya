import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabaz_score, davies_bouldin_score, silhouette_score

# GLOBALS
max_k = 20
best = {'k': 0, 'centers': [], 'err': -1, 'errmode': 0}
# determines how error is calculated
errmethods = ['Davies-Bouldin', 'Calinski-Harabasz', 'Silhouette', 'S_Dbw (incomplete!)']
errmode = 2 # index of error method in errmethods
worst_err = -1

print("Error method in use: " + errmethods[errmode])




# DATA IMPORT
# read data from file and crop
dcsv = open('data.csv','r')
data = np.genfromtxt(dcsv, delimiter=',', dtype=None, encoding='unicode')
dcsv.close()
data = data[1:,6:]



# DATA FORMAT
# convert sex data points and age data points to numbers
sex = age = None
sexvals = ['f', 'm']
agevals = ['20s', '30s', '40s', '50s', '60s', '70s']
for i in range(data[0].size):
    if (data[0][i] in sexvals):
        sex = i
    elif (data[0][i] in agevals):
        age = i

if (sex != None):
    for i in range(data[:,sex].size):
        data[i,sex] = sexvals.index(data[i,sex])

if (age != None):
    for i in range(data[:,age].size):
        data[i,age] = agevals.index(data[i,age])

#clean rest of data
cols = []

# find any non-number columns
for i in range(data[0].size):
    if not (str.isdigit(data[0][i]) or isinstance(data[0][i], int) or isinstance(data[0][i], float)):
        cols.append(i)

# delete non-number columns
for i in range(len(cols)):
    data = np.delete(data, cols[i], 1)

# convert from string to float
data = data.astype(float)


# FIND CLUSTERS
# error file
elog = open("error_log.csv", "w")
elog.write("k,err," + errmethods[errmode] + '\n')

# function to calculate different error measures
def error(data, centers, labels):
    if errmode == 0:
        # Davies-Bouldin
        return(davies_bouldin_score(data, labels))
    elif errmode == 1:
        # Calinski-Harabasz
        return(calinski_harabaz_score(data, labels))
    elif errmode == 2:
        # Silhouette
        return(silhouette_score(data, labels))
    elif errmode == 3:
        #S_Dbw
        #TODO
        return(1)
    else:
        print("Invalid error mode.")
        sys.exit()

# function to check given error measure against current best solutions error measure
def check_error(cur, mode='good'):
    # if using Calinski-Harabasz or Silhouette, better solutions maximize error index
    if (errmode==1 or errmode==2):
        if (mode=='good'):
            return(cur>best['err'])
        else:
            return(cur<worst_err)

    # if using Davies-Bouldin or S_Dbw, better solutions minimize error index
    else:
        if (mode=='good'):
            return(cur<best['err'])
        else:
            return(cur>worst_err)


# clustering algorithm and solution tracking
for k in range(2, max_k+1):
    # run kmeans algorithm with given k
    kmeans = KMeans(n_clusters=k).fit(data)

    # calculate quality of result
    cur_err = error(data, kmeans.cluster_centers_, kmeans.labels_)

    # if the error is closer to optimal than existing best solution, update best
    if (best['err']<0 or check_error(cur_err)):
        best['k'] = k
        best['centers'] = kmeans.cluster_centers_
        best['err'] = cur_err

    # if the error is worse than the existing worst solution, update worst error
    elif (check_error(cur_err, mode='bad') or worst_err<0):
        worst_err = cur_err
    
    # log error
    elog.write(str(k) + ',' + str(cur_err) + '\n')


# solution file
np.savetxt('solution.csv', best['centers'], delimiter=',')

print("Optimal solution found, maybe!")
print('k = ', best['k'], '\nerr = ', best['err'], '\nerrmode = ', best['errmode'], '\nworst = ', worst_err)
