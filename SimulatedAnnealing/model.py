import numpy as np
import pandas as pd
from sklearn.utils import shuffle

# Read dataset
dataset = pd.read_csv('dataset.csv')
dataset = shuffle(dataset)
dataset = dataset.reset_index(drop=True)

# print(dataset)
# print(dataset.describe(include='all'))

X_original = dataset[['window', 'negative', 'batch-size', 'threads']]
y_original = dataset['time'].values

# print(X_original)
# print(y_original)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X = scaler.fit_transform(X_original)
y = y_original.reshape(-1,1)
y = scaler.fit_transform(y)

# print(X)
# print(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

from keras import Sequential
from keras.layers import Dense
def create_model():
    regressor = Sequential()
    regressor.add(Dense(units=32, input_dim=4, activation='relu'))
    regressor.add(Dense(units=1, activation='linear'))
    regressor.compile(optimizer='adam', loss='mean_squared_error',  metrics=['mae', 'mse'])
    return regressor

model = create_model()

history = model.fit(X_train, y_train, batch_size=32, epochs=100, validation_data=(X_test, y_test))

model.save('model.h5')