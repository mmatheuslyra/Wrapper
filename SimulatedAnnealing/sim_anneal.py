from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

import numpy as np
import pandas as pd
import math
import random
import copy

# Read dataset
dataset = pd.read_csv('dataset.csv')
X_original = dataset[['window', 'negative', 'batch-size', 'threads']]
y_original = dataset['time'].values
X_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()
X = X_scaler.fit_transform(X_original)
y = y_original.reshape(-1,1)
y = y_scaler.fit_transform(y)

# Objective function
model = load_model('model.h5')
def f(x):
    x = X_scaler.transform(np.array(x).reshape(1,-1))
    pred = model.predict(x)
    return y_scaler.inverse_transform(pred[0].reshape(-1,1))[0][0]

# ['window', 'negative', 'batch-size', 'threads']
upper_bound = [9, 25, 20, 48]
lower_bound = [5, 5, 10, 6]

# Transition function
def step(x):
    x_best = None
    f_best = float('inf')
    for i in range(4):
        x_add = copy.deepcopy(x)
        x_sub = copy.deepcopy(x)
        if i == 0: 
            step_size = 1
        elif i == 1: 
            step_size = 3
        elif i == 2: 
            step_size = 2
        elif i == 3: 
            step_size = 4

        x_add[i] = x_add[i] + step_size
        x_sub[i] = x_sub[i] - step_size
        f_add = f(x_add)
        f_sub = f(x_sub)

        if x_add[i] > upper_bound[i]: f_add = float('inf')
        if x_sub[i] < lower_bound[i]: f_sub = float('inf')

        
        if f_add <= f_sub and f_add <= f_best: 
            x_best = x_add
            f_best = f_add
        elif f_sub <= f_best:
            x_best = x_sub
            f_best = f_sub
    return x_best, f_best

# print(f([5,5,10,48]))
# [5, 5, 10, 48]: 37.12850332
# [0., 0.04761905, 0.1, 1.]: 0.0592102

# Hyperparams
T = 10
T_decay = 0.9
n = 10
m = 100
na = 0
DeltaE_avg = 0.0

# Initialize
x = [9,21,17,10]
fx = f(x)
x_history = [x]
fx_history = [fx]

for i in range(n):

    print('Cycle: ' + str(i) + ' with Temperature: ' + str(T) + '\t| x = ' + str(x) + '\tfx = ' + str(fx))

    for j in range(m):

        # New candidate
        x_prime, fx_prime = step(x)

        DeltaE = abs(fx_prime-fx)

        if (fx_prime > fx):
            # Initialize DeltaE_avg if a worse solution was found on the first iteration
            if (i==0 and j==0): DeltaE_avg = DeltaE
            # objective function is worse
            # generate probability of acceptance
            p = math.exp(-DeltaE/(DeltaE_avg * T))
            # determine whether to accept worse point
            if random.random() < p:
                # accept the worse solution
                accept = True
            else:
                # don't accept the worse solution
                accept = False
        else:
            # objective function is lower, automatically accept
            accept = True
        if accept == True:
            # update currently accepted solution
            x = x_prime
            fx = fx_prime
            # increment number of accepted solutions
            na = na + 1.0
            # update DeltaE_avg
            DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na

    T = T_decay * T
    x_history.append(x)
    fx_history.append(fx)