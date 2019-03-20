# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np

class DataNormalizer(object):
    def __init__(self, method):
        assert(method == "min_max")
        self.method = method

    # normalize data by extracting range from source data
    # return: X_new: normalized data with same shape
    # return: X_norm: 2xN (features)
    #               [[min1, min2, min3...]
    #                [range1, range2, range3...]]
    def NormalizeData(self, X_raw):
        X_new = np.zeros(X_raw.shape)
        num_feature = X_raw.shape[0]
        self.X_norm = np.zeros((2,num_feature))
        # 按行归一化,即所有样本的同一特征值分别做归一化
        for i in range(num_feature):
            # get one feature from all examples
            x = X_raw[i,:]
            max_value = np.max(x)
            min_value = np.min(x)
            # min value
            X_norm[0,i] = min_value 
            # range value
            self.X_norm[1,i] = max_value - min_value 
            x_new = (x - self.X_norm[0,i]) / self.X_norm[1,i]
            X_new[i,:] = x_new
        # end for
        return X_new

    # normalize data by specified range and min_value
    def NormalizePredicateData(self, X_raw):
        X_new = np.zeros(X_raw.shape)
        num_feature = X_raw.shape[0]
        for i in range(num_feature):
            x = X_raw[i,:]
            X_new[i,:] = (x-self.X_norm[0,i])/self.X_norm[1,i]
        return X_new
