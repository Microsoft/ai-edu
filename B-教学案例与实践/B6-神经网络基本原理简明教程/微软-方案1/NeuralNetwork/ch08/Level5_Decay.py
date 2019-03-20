# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import math
from LossFunction import * 
from Utility import *
from Activations import *

x_data_name = "CurveX.dat"
y_data_name = "CurveY.dat"


def ForwardCalculationBatch(batch_x, dict_weights):
    W1 = dict_weights["W1"]
    B1 = dict_weights["B1"]
    W2 = dict_weights["W2"]
    B2 = dict_weights["B2"]

    Z1 = np.dot(W1, batch_x) + B1
    A1 = CSigmoid().forward(Z1)

    Z2 = np.dot(W2, A1) + B2
    A2 = Z2

    dict_cache ={"A1": A1, "A2": A2, "Output": A2}
    return dict_cache

def BackPropagationBatch(batch_x, batch_y, dict_cache, dict_weights):
    # 批量下降，需要除以样本数量，否则会造成梯度爆炸
    m = batch_x.shape[1]
    # 取出缓存值
    A1 = dict_cache["A1"]
    A2 = dict_cache["A2"]
    W2 = dict_weights["W2"]
    # 第二层的梯度
    dZ2 = A2 - batch_y
    # 第二层的权重和偏移
    dW2 = np.dot(dZ2, A1.T)/m
    dB2 = np.sum(dZ2, axis=1, keepdims=True)/m
    # 第一层的梯度
    dA1 = np.dot(W2.T, dZ2)
    dA1_Z1 = np.multiply(A1, 1 - A1)
    dZ1 = np.multiply(dA1, dA1_Z1)
    # 第一层的权重和偏移
    dW1 = np.dot(dZ1, batch_x.T)/m
    dB1 = np.sum(dZ1, axis=1, keepdims=True)/m
    # 保存到词典中返回
    dict_grads = {"dW1":dW1, "dB1":dB1, "dW2":dW2, "dB2":dB2}
    return dict_grads

def UpdateWeights(dict_weights, dict_grads, learningRate):
    W1 = dict_weights["W1"]
    B1 = dict_weights["B1"]
    W2 = dict_weights["W2"]
    B2 = dict_weights["B2"]

    dW1 = dict_grads["dW1"]
    dB1 = dict_grads["dB1"]
    dW2 = dict_grads["dW2"]
    dB2 = dict_grads["dB2"]

    W1 = W1 - learningRate * dW1
    W2 = W2 - learningRate * dW2
    B1 = B1 - learningRate * dB1
    B2 = B2 - learningRate * dB2

    dict_weights = {"W1": W1,"B1": B1,"W2": W2,"B2": B2}

    return dict_weights

def ShowResult(X, Y, dict_weights):
    # draw train data
    plt.plot(X[0,:], Y[0,:], '.', c='b')
    # create and draw visualized validation data
    TX = np.linspace(0,1,100).reshape(1,100)
    dict_cache = ForwardCalculationBatch(TX, dict_weights)
    TY = dict_cache["Output"]
    plt.plot(TX, TY, 'x', c='r')
    plt.show()

def GetLearningRate(epoch, iteration, max_iteration, eta_0):
    
    #alpha = (epoch * max_iteration + iteration)/500
    #eta_k = (1-alpha)*eta_0 + alpha * eta / 100
    eta_k = eta_0 / (1 + 0.0001 * epoch)
    return eta_k

def train(X, Y, params, loss_history):
    num_example = X.shape[1]
    num_feature = X.shape[0]
    num_category = Y.shape[0]

    # W(num_category, num_feature), B(num_category, 1)
    W1, B1 = InitialParameters(params.num_input, params.num_hidden, params.init_method)
    W2, B2 = InitialParameters(params.num_hidden, params.num_output, params.init_method)
    dict_weights = {"W1":W1, "B1":B1, "W2":W2, "B2":B2}

    # calculate loss to decide the stop condition
    loss = 0 
    lossFunc = CLossFunction(params.loss_func_type)

    # if num_example=200, batch_size=10, then iteration=200/10=20
    max_iteration = (int)(params.num_example / params.batch_size)
    for epoch in range(params.max_epoch):
        for iteration in range(max_iteration):
            eta = GetLearningRate(epoch, iteration, max_iteration, params.eta)
            # get x and y value for one sample
            batch_x, batch_y = GetBatchSamples(X,Y,params.batch_size,iteration)
            # get z from x,y
            dict_cache = ForwardCalculationBatch(batch_x, dict_weights)
            # calculate gradient of w and b
            dict_grads = BackPropagationBatch(batch_x, batch_y, dict_cache, dict_weights)
            # update w,b
            dict_weights = UpdateWeights(dict_weights, dict_grads, eta)
        # end for            
        # calculate loss for this batch
        loss = lossFunc.CheckLoss(X, Y, dict_weights, ForwardCalculationBatch)
        print("epoch=%d, eta=%f, loss=%f" %(epoch,eta,loss))
        loss_history.AddLossHistory(loss, dict_weights, epoch, iteration)            
        if math.isnan(loss):
            break
        # end if
        if loss < params.eps:
            break
        # end if
    # end for
    return dict_weights

if __name__ == '__main__':

    X,Y = ReadData(x_data_name, y_data_name)
    num_example = X.shape[1]
    n_input, n_hidden, n_output = 1, 4, 1
    eta, batch_size, max_epoch = 0.1, 10, 50000
    eps = 0.001
    init_method = 2

    params = CParameters(num_example, n_input, n_output, n_hidden, eta, max_epoch, batch_size, "MSE", eps, init_method)

    # SGD, MiniBatch, FullBatch
    loss_history = CLossHistory()
    dict_weights = train(X, Y, params, loss_history)

    bookmark = loss_history.GetMinimalLossData()
    bookmark.print_info()
    loss_history.ShowLossHistory(params)

    ShowResult(X, Y, bookmark.weights)
    print(bookmark.weights["W1"])
    print(bookmark.weights["B1"])
    print(bookmark.weights["W2"])
    print(bookmark.weights["B2"])

