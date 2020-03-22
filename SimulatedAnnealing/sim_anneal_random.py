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
X_scaler = MinMaxScaler()   # Objeto MinMaxScaler 
y_scaler = MinMaxScaler()
X = X_scaler.fit_transform(X_original) # Normalizar os valores para a rede treinar melhor 
y = y_original.reshape(-1,1) # pra bater com a entrada da rede
y = y_scaler.fit_transform(y)

# Objective function
model = load_model('model.h5')
def f(x):
    x = X_scaler.transform(np.array(x).reshape(1,-1)) #pra bater com a entrada da rede
    pred = model.predict(x)
    return y_scaler.inverse_transform(pred[0].reshape(-1,1))[0][0] # Reverte a normalização

# ['window', 'negative', 'batch-size', 'threads']
upper_bound = [9, 25, 20, 48]
lower_bound = [5, 5, 10, 6]

# Transition function
def step(x):
    step_size = 1

    #Choose randomly which parameter will be updated and if it'll be up or down
    param = random.randrange(0,4,1)
    up_down = random.randrange(0,2,1)

    x_step = copy.deepcopy(x)

    if param == 0: 
        pass #return x, f(x) #pass
    elif param == 1:
        pass #return x, f(x)
    elif param == 2: 
        pass #return x, f(x)
    elif param == 3:
        pass #return x, f(x)

    if up_down == 0:
        x_step[param] -= step_size
        if x_step[param] < lower_bound[param]: x_step[param] += step_size
    else:
        x_step[param] += step_size
        if x_step[param] > upper_bound[param]: x_step[param] -= step_size

    fx_step = f(x_step)

    return x_step, fx_step

# Hyperparams
T = 100 #10 # investigar a temperatura
T_decay = 0.98 #0.9
n = 350 #50
m = 250 #10
na = 0
DeltaE_avg = 0.0

# Initialize
# x = [9,15,15,15]
x = [9,10,10,10]

fx = f(x)
x_history = [x]
fx_history = [fx]

for i in range(n):
    print('Cycle: ' + str(i) + ' with Temperature: ' + str(T) + '\t| x = ' + str(x) + '\tfx = ' + str(fx))

    for j in range(m):

        # New candidate
        x_prime, fx_prime = step(x)

        DeltaE = abs(fx_prime-fx) # Calculo do Erro

        if (fx_prime > fx):
            # Initialize DeltaE_avg if a worse solution was found on the first iteration
            if (i==0 and j==0): DeltaE_avg = DeltaE
            # objective function is worse
            # generate probability of acceptance
            p = math.exp(-DeltaE/(DeltaE_avg * T))  ##A probabilidade atua sobre a aceitação do próximo estado
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
