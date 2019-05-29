# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from MiniFramework.NeuralNet import *
from MiniFramework.Optimizer import *
from MiniFramework.LossFunction import *
from MiniFramework.Parameters import *
from MiniFramework.WeightsBias import *
from MiniFramework.ActivatorLayer import *
from MiniFramework.DataReader import *


train_file = "../../Data/09_Train.npz"
test_file = "../../Data/09_Test.npz"


def ShowResult(net, dataReader, title):
    # draw train data
    plt.plot(dataReader.XTrain[:,0], dataReader.YTrain[:,0], '.', c='b')
    plt.plot(dataReader.XTest[:,0], dataReader.YTest[:,0], '.', c='g')
    # create and draw visualized validation data
    TX = np.linspace(0,1,100).reshape(100,1)
    TY = net.inference(TX)
    plt.plot(TX, TY, 'x', c='r')
    plt.title(title)
    plt.show()

def LoadData():
    dr = DataReader(train_file, test_file)
    dr.ReadData()
    #dr.NormalizeX()
    #dr.NormalizeY(YNormalizationMethod.Regression)
    dr.Shuffle()
    dr.GenerateValidationSet()
    return dr

if __name__ == '__main__':
    dataReader = LoadData()
    num_input = 1
    num_hidden1 = 4
    num_output = 1

    max_epoch = 10000
    batch_size = 10
    learning_rate = 0.1
    eps = 0.001

    params = CParameters(learning_rate, max_epoch, batch_size, eps,
                        LossFunctionName.MSE, 
                        InitialMethod.Xavier, 
                        OptimizerName.Momentum)

    net = NeuralNet(params, "Level1_CurveFittingNet")
    fc1 = FcLayer(num_input, num_hidden1, params)
    net.add_layer(fc1, "fc1")
    sigmoid1 = ActivatorLayer(Sigmoid())
    net.add_layer(sigmoid1, "sigmoid1")
    fc2 = FcLayer(num_hidden1, num_output, params)
    net.add_layer(fc2, "fc2")

    net.train(dataReader, checkpoint=100, need_test=True)
    net.ShowLossHistory()
    
    ShowResult(net, dataReader, params.toString())
