# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np

from HelperClass.NeuralNet import *
from HelperClass.HyperParameters import *

   
# 主程序
if __name__ == '__main__':
    # data
    reader = SimpleDataReader()
    reader.ReadData()
    # net
    params = HyperParameters(eta=0.1, max_epoch=100, batch_size=10, eps=1e-3, net_type=NetType.BinaryClassifier)
    input = 2
    output = 1
    net = NeuralNet(params, input, output)
    net.train(reader, checkpoint=1)

    # inference
    x_predicate = np.array([0.58,0.92,0.62,0.55,0.39,0.29]).reshape(3,2)
    a = net.inference(x_predicate)
    print("A=", a)




