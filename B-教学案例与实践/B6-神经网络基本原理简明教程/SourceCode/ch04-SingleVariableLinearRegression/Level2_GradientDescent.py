# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# 用单次迭代方式
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from HelperClass.SimpleDataReader import *

if __name__ == '__main__':

    reader = SimpleDataReader()
    reader.ReadData()
    X,Y = reader.GetWholeTrainSamples()

    eta = 0.1
    w, b = 0.0, 0.0
    #w,b = np.random.random(),np.random.random()
    # count of samples
    num_example = X.shape[0]
    for i in range(num_example):
        # get x and y value for one sample
        x = X[i]
        y = Y[i]
        # get z from x,y
        z = x*w+b
        # calculate gradient of w and b
        dz = z - y
        db = dz
        dw = dz * x
        # update w,b
        w = w - eta * dw
        b = b - eta * db

    print("w=", w)    
    print("b=", b)