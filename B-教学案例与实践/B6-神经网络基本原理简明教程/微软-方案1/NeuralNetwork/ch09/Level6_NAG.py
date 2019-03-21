# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import math
from LossFunction import * 
from Parameters import *
from Activations import *
from Level1_TwoLayer import *

x_data_name = "X3.npy"
y_data_name = "Y3.npy"

class CNag(object):
    def __init__(self, eta):
        self.vt_1 = 0
        self.eta = eta
        self.gamma = 0.9

    # 先用预测的梯度来更新W,b
    def step1(self, theta):
        theta = theta + self.gamma * self.vt_1
        return theta

    # 再用动量法更新W,b
    def step2(self, theta, grad):
        vt = self.gamma * self.vt_1 - self.eta * grad
        theta = theta + vt
        self.vt_1 = vt
        return theta


class CNagOptimizer(CTwoLayerNet):
    def UpdateWeights_1(self, dict_weights, dict_nag):
        W1 = dict_weights["W1"]
        B1 = dict_weights["B1"]
        W2 = dict_weights["W2"]
        B2 = dict_weights["B2"]

        W1 = dict_nag["W1"].step1(W1)
        B1 = dict_nag["B1"].step1(B1)
        W2 = dict_nag["W2"].step1(W2)
        B2 = dict_nag["B2"].step1(B2)

        dict_weights = {"W1": W1,"B1": B1,"W2": W2,"B2": B2}

        return dict_weights

    def UpdateWeights_2(self, dict_weights, dict_grads, dict_nag):
        W1 = dict_weights["W1"]
        B1 = dict_weights["B1"]
        W2 = dict_weights["W2"]
        B2 = dict_weights["B2"]

        dW1 = dict_grads["dW1"]
        dB1 = dict_grads["dB1"]
        dW2 = dict_grads["dW2"]
        dB2 = dict_grads["dB2"]

        W1 = dict_nag["W1"].step2(W1, dW1)
        B1 = dict_nag["B1"].step2(B1, dB1)
        W2 = dict_nag["W2"].step2(W2, dW2)
        B2 = dict_nag["B2"].step2(B2, dB2)

        dict_weights = {"W1": W1,"B1": B1,"W2": W2,"B2": B2}

        return dict_weights


    def train(self, X, Y, params, loss_history):
        num_example = X.shape[1]
        num_feature = X.shape[0]
        num_category = Y.shape[0]

        # W(num_category, num_feature), B(num_category, 1)
        W1, B1, W2, B2 = params.LoadSameInitialParameters()
        dict_weights = {"W1":W1, "B1":B1, "W2":W2, "B2":B2}
        dict_nag = {"W1":CNag(params.eta), "B1":CNag(params.eta), "W2":CNag(params.eta), "B2":CNag(params.eta)}

        # calculate loss to decide the stop condition
        loss = 0 
        lossFunc = CLossFunction(params.loss_func_name)

        # if num_example=200, batch_size=10, then iteration=200/10=20
        max_iteration = (int)(params.num_example / params.batch_size)
        for epoch in range(params.max_epoch):
            for iteration in range(max_iteration):
                # get x and y value for one sample
                batch_x, batch_y = DataOperator.GetBatchSamples(X,Y,params.batch_size,iteration)

                # nag
                dict_weights = self.UpdateWeights_1(dict_weights, dict_nag)

                # get z from x,y
                dict_cache = self.ForwardCalculationBatch(batch_x, dict_weights)

                # calculate gradient of w and b
                dict_grads = self.BackPropagationBatch(batch_x, batch_y, dict_cache, dict_weights)
                # update w,b
                dict_weights = self.UpdateWeights_2(dict_weights, dict_grads, dict_nag)
            # end for            
            # calculate loss for this batch
            loss = lossFunc.CheckLoss(X, Y, dict_weights, self.ForwardCalculationBatch)
            print("epoch=%d, loss=%f" %(epoch,loss))
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

    XData,YData = DataOperator.ReadData(x_data_name, y_data_name)
    norm = DataOperator("min_max")
    X = norm.NormalizeData(XData)
    num_category = 3
    Y = DataOperator.ToOneHot(YData, num_category)

    num_example = X.shape[1]
    num_feature = X.shape[0]
    
    n_input, n_hidden, n_output = num_feature, 8, num_category
    eta, batch_size, max_epoch = 0.5, 500, 80000
    eps = 0.05
    init_method = InitialMethod.xavier

    params = CParameters(num_example, n_input, n_output, n_hidden, eta, max_epoch, batch_size, LossFunctionName.CrossEntropy3, eps, init_method)

    loss_history = CLossHistory()
    optimizer = CNagOptimizer()
    dict_weights = optimizer.train(X, Y, params, loss_history)

    bookmark = loss_history.GetMinimalLossData()
    bookmark.print_info()
    loss_history.ShowLossHistory(params)

    optimizer.ShowAreaResult(X, bookmark.weights)
    optimizer.ShowData(X, YData)

