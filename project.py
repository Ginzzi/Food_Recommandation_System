#!/usr/bin/env python
# coding: utf-8



import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.callbacks import CSVLogger
import matplotlib.pyplot as plt




fi = open('keptcolumns.txt', 'r')
keptcolumns = fi.read().rstrip('\n').split(', ')
keptcolumns = np.array(keptcolumns)
data = pd.read_csv('epi_r_toy.csv', usecols = keptcolumns)
# data = pd.read_csv('epi_r.csv', usecols = keptcolumns) # comment out if you want to use the original dataset 
data = data[pd.notnull(data['calories'])]
data = data[pd.notnull(data['protein'])]
data = data[pd.notnull(data['fat'])]
data = data[data['calories'] != 0]
data = data[data['protein'] != 0]
data = data[data['fat'] != 0]
data = data.values
h_val = data[:, 0:6]
ingred = data[:, 6:]




def gen_dat(xy):
    cnt = np.sum(xy == 1)
    idx = np.where(xy == 1)
    x = np.zeros((cnt, xy.shape[0]))
    y = np.zeros((cnt, xy.shape[0]))
    for i in range(cnt):
        y_idx = idx[0][i]
        x_idx = np.setdiff1d(idx[0], y_idx)
        y[i, y_idx] = 1
        x[i, x_idx] = 1
    return x, y




x = np.empty((0, ingred.shape[1]))
y = np.empty((0, ingred.shape[1]))
for i in range(ingred.shape[0]):
    x_tmp, y_tmp = gen_dat(ingred[i])
    x = np.append(x, x_tmp, axis = 0)
    y = np.append(y, y_tmp, axis = 0)
print(x.shape)
print(y.shape)




idx = np.arange(x.shape[0])
np.random.shuffle(idx)
x = x[idx]
y = y[idx]
p = x.shape[0] * 8 // 10
x_train = x[:p, :]
y_train = y[:p, :]
x_test = x[p:, :]
y_test = y[p:, :]
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)




model1 = Sequential([Dense(200, input_shape=(308,)),
                                    LeakyReLU(),
                                    
                                    Dense(300),
                                    LeakyReLU(),
                                    
                                    Dense(300),
                                    LeakyReLU(),
                                                                                                            
                                    Dense(300),
                                    LeakyReLU(),
                                    
                                    Dense(300),
                                    LeakyReLU(),
                                    
                                    Dense(308, activation='sigmoid')
                                   ])
model1.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['categorical_accuracy'])
model1.summary()




csv_logger = CSVLogger('training1.log')
model1.fit(x_train, y_train, epochs = 22, batch_size = 128, callbacks = [csv_logger])




x = ingred
calories = h_val[:, 2]
protein = h_val[:, 3]
fat = h_val[:, 4]
y = protein / (calories * fat)
print(np.where(y == 0))
idx = np.argsort(y)
idx = idx[:-250]
np.random.shuffle(idx)
x = x[idx]
y = y[idx]
maxi = np.max(y)
y = y / maxi




model2 = Sequential([Dense(200, input_shape=(308,)),
                                    LeakyReLU(),
                                    
                                    Dense(500),
                                    LeakyReLU(),
                                    
                                    Dense(500),
                                    LeakyReLU(),
                    
                                    Dense(500),
                                    LeakyReLU(),
                    
                                    Dense(500),
                                    LeakyReLU(),
                    
                                    Dense(500),
                                    LeakyReLU(),
                                                        
                                    Dense(1)
                                   ])
model2.compile(optimizer='adam', loss='mean_squared_error')
model2.summary()




csv_logger = CSVLogger('training2.log')
model2.fit(x, y, epochs = 22, batch_size=1024, callbacks=[csv_logger])




cnt1 = 0
cnt2 = 0
for i in range(x_test.shape[0]):
    x = x_test[i].reshape(1, x_test.shape[1])
    y = model1.predict(x, batch_size = 128)
    y_idx = np.argsort(y[0])
    y_idx = y_idx[-20:]
    if np.where(y_test[i] == 1) in y_idx:
        cnt1 += 1
    cnt2 += 1
print(cnt1 / cnt2)




cnt1 = 0
cnt2 = 0
for i in range(x_train.shape[0]):
    x = x_train[i].reshape(1, x_train.shape[1])
    y = model1.predict(x, batch_size = 128)
    y_idx = np.argsort(y[0])
    y_idx = y_idx[-20:]
    if np.where(y_train[i] == 1) in y_idx:
        cnt1 += 1
    cnt2 += 1
print(cnt1 / cnt2)




def test_model(x_idx):
    x = np.zeros((1, ingred.shape[1]))
    x[0, x_idx] = 1
    y = model1.predict(x, batch_size = 128)
    y_idx = np.argsort(y[0])
    y_idx = y_idx[-5:]
    print('Initial Suggestions: ')
    print(keptcolumns[y_idx + 6])
    print('Scores: ')
    print(y[0][y_idx])
    h_val = np.zeros(5)
    for i in range(5):
        x_tmp = np.append(x_idx, y_idx[i])
        x = np.zeros((1, 308))
        x[0, x_tmp] = 1        
        y_tmp = model2.predict(x, batch_size = 128)
        h_val[i] = y_tmp
    y_idx_idx = np.argsort(h_val)
    y_idx = y_idx[y_idx_idx]
    print('Final Suggestions Based on Health: ')
    print(keptcolumns[y_idx + 6])
    print('Health values: ')
    print(h_val[y_idx_idx])




rec_no = 78
print("Recipe name: ", h_val[rec_no][0])
idx = np.array(np.where(ingred[rec_no] == 1))
print("Original Ingredients: ")
print(keptcolumns[idx + 6])
test_model(np.array([49, 93, 118, 263, 294]))






