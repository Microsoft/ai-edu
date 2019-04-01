# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import math

from LossFunction import * 
from Activators import *
from Level0_TwoLayerClassificationNet import *
from DataReader import * 
from WeightsBias import *


# x1=0,x2=0,y=0
# x1=0,x2=1,y=1
# x1=1,x2=0,y=1
# x1=1,x2=1,y=0
class XOR_DataReader():
    def __init__(self):
        pass

    def ReadData(self):
        self.X = np.array([0,0,1,1,0,1,0,1]).reshape(2,4)
        self.Y = np.array([0,1,1,0]).reshape(1,4)
        self.num_example = self.X.shape[1]
        self.num_feature = self.X.shape[0]
        self.num_category = 1

    def GetBatchSamples(self, batch_size, iteration):
        start = iteration * batch_size
        end = start + batch_size
        batch_X = self.X[0:self.num_feature, start:end].reshape(self.num_feature, batch_size)
        batch_Y = self.Y[:, start:end].reshape(-1, batch_size)
        return batch_X, batch_Y


def ShowAreaResult(net, wb1, wb2, title):
    count = 50
    x1 = np.linspace(0,1,count)
    x2 = np.linspace(0,1,count)
    for i in range(count):
        for j in range(count):
            x = np.array([x1[i],x2[j]]).reshape(2,1)
            dict_cache = net.ForwardCalculationBatch2(x, wb1, wb2)
            output = dict_cache["Output"]
            if output[0,0] >= 0.5:
                plt.plot(x[0,0], x[1,0], 's', c='m')
            else:
                plt.plot(x[0,0], x[1,0], 's', c='y')
            # end if
        # end for
    # end for
    plt.title(title)
#end def

def ShowData(X, Y):
    for i in range(X.shape[1]):
        if Y[0,i] == 0:
            plt.plot(X[0,i], X[1,i], '^', c='r')
        elif Y[0,i] == 1:
            plt.plot(X[0,i], X[1,i], '.', c='g')
        # end if
    # end for
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.show()

    
def LoadWeights(wb1, wb2):
    wb1.W = np.load("xor_w1_2_2.npy")
    wb1.B = np.load("xor_w1_2_1.npy")
    wb2.W = np.load("xor_w2_1_2.npy")
    wb2.B = np.load("xor_w2_1_1.npy")


def ShowZ1A1Z2A2():
    wb1 = WeightsBias(2,2,0.1,InitialMethod.Xavier)
    wb2 = WeightsBias(1,2,0.1,InitialMethod.Xavier)
    LoadWeights(wb1, wb2)
    print(wb1.toString())    
    print(wb2.toString())

    dataReader = XOR_DataReader()
    dataReader.ReadData()

    
    Z1 = np.dot(wb1.W, dataReader.X) + wb1.B
    A1 = Sigmoid().forward(Z1)
    # layer 2
    Z2 = np.dot(wb2.W, A1) + wb2.B
    A2 = Sigmoid().forward(Z2)
    print(Z1)
    print(A1)
    print(Z2)
    print(A2)

    for i in range(dataReader.num_example):
        if dataReader.Y[0,i] == 0:
            plt.plot(dataReader.X[0,i],dataReader.X[1,i],'^',c='r')
        else:
            plt.plot(dataReader.X[0,i],dataReader.X[1,i],'o',c='g')
    plt.grid()
    plt.title("X1:X2")
    plt.show()


    for i in range(dataReader.num_example):
        if dataReader.Y[0,i] == 0:
            plt.plot(Z1[0,i],Z1[1,i],'^',c='r')
        else:
            plt.plot(Z1[0,i],Z1[1,i],'o',c='g')
    plt.grid()
    plt.title("Z1")
    plt.show()


    for i in range(dataReader.num_example):
        if dataReader.Y[0,i] == 0:
            plt.plot(A1[0,i],A1[1,i],'^',c='r')
        else:
            plt.plot(A1[0,i],A1[1,i],'o',c='g')
    plt.grid()
    plt.title("A1")
    plt.show()

    x = np.linspace(-6,6)
    a = Sigmoid().forward(x)
    plt.plot(x,a)

    for i in range(dataReader.num_example):
        if dataReader.Y[0,i] == 0:
            plt.plot(Z2[0,i],A2[0,i],'^',c='r')
        else:
            plt.plot(Z2[0,i],A2[0,i],'o',c='g')
    plt.grid()
    plt.title("Z2:A2")
    plt.show()


if __name__ == '__main__':
    # 每次运行之前，需要把level1中的Line 98, max_epoch的数字从小改到大，比如200,400,600,800,1000,...，
    # 每改一次max_epoch，运行一次level1，生成权重值并自动保存，再运行一次本程序绘图
    ShowZ1A1Z2A2()