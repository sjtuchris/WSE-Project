from __future__ import print_function, division
import os
import torch
import pandas as pd
import numpy as np
import torch.nn.functional as F     # 激励函数都在这
import matplotlib.pyplot as plt
import torch.utils.data as Data
from torchvision import transforms, utils
from torch.autograd import Variable # torch 中 Variable 模块
from sklearn import preprocessing



# # Ignore warnings
# import warnings
# warnings.filterwarnings("ignore")

class Net(torch.nn.Module):     # 继承 torch 的 Module
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()     # 继承 __init__ 功能
        self.hidden = torch.nn.Linear(n_feature, n_hidden)   # 隐藏层线性输出
        self.out = torch.nn.Linear(n_hidden, n_output)       # 输出层线性输出

    def forward(self, x):
        # 正向传播输入值, 神经网络分析出输出值
        x = F.relu(self.hidden(x))      # 激励函数(隐藏层的线性值)
        x = self.out(x)                 # 输出值, 但是这个不是预测值, 预测值还需要再另外计算
        return x

def train_classifer():
    net = Net(n_feature=6, n_hidden=10, n_output=2) # 几个类别就几个 output

    features_set = pd.read_csv('new.csv', dtype = float, usecols=['backers_count','comment_num','goal','period','pledged','update'])
    results_set = pd.read_csv('new.csv', usecols=['state'])


    # normalize features
    min_max_scaler = preprocessing.MinMaxScaler()
    features_scaled = min_max_scaler.fit_transform(features_set.values)

    features_tensor = torch.FloatTensor(features_scaled)

    features = Variable(features_tensor)

    results_tensor = torch.LongTensor(results_set.values.flatten())
    results = Variable(results_tensor)

    BATCH_SIZE = 5
    torch_dataset = Data.TensorDataset(data_tensor=features_tensor, target_tensor=results_tensor)
    loader = Data.DataLoader(
        dataset=torch_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=2,
        )

    optimizer = torch.optim.SGD(net.parameters(), lr=0.1)  # 传入 net 的所有参数, 学习率
    # 算误差的时候, 注意真实值!不是! one-hot 形式的, 而是1D Tensor, (batch,)
    # 但是预测值是2D tensor (batch, n_classes)
    loss_func = torch.nn.CrossEntropyLoss()

    # for t in range(2000):
    for epoch in range(3):
        for step, (batch_x, batch_y) in enumerate(loader):
            out = net(Variable(batch_x))     # 喂给 net 训练数据 x, 输出分析值

            loss = loss_func(out, Variable(batch_y))     # 计算两者的误差

            optimizer.zero_grad()   # 清空上一步的残余更新参数值
            loss.backward()         # 误差反向传播, 计算参数更新值
            optimizer.step()        # 将参数更新值施加到 net 的 parameters 上

            print('Epoch: ', epoch, '| Step: ', step, '| batch x: ',
              batch_x.numpy(), '| batch y: ', batch_y.numpy())

    out = net(features)
    prediction = torch.max(F.softmax(out), 1)[1]
    # print(prediction)
    pred_y = prediction.data.numpy().squeeze()
    # np.set_printoptions(threshold=np.inf)
    print(sum(abs(pred_y-results_set.values.flatten()))/len(pred_y))
    torch.save(net.state_dict(), "net")

def predict():
    net = Net(n_feature=6, n_hidden=10, n_output=2) # 几个类别就几个 output
    net.load_state_dict(torch.load("net"))
    # features_set = [4,0,30000,0,28,56]
    features_set = [[4,0,30000,0,28,56],[648,68,11000,16,31,24000],[4,0,30000,0,28,56],[0,0,3500,0,60,0]]
    # features_set = [[1,0,3500000,0,33,10]]

    min_max_scaler = preprocessing.MinMaxScaler()
    features_scaled = min_max_scaler.fit_transform(features_set)

    features_tensor = torch.FloatTensor(features_scaled)
    features = Variable(features_tensor)

    out = net(features)
    print(F.softmax(out))
    prediction = torch.max(F.softmax(out), 1)[1]
    pred_y = prediction.data.numpy().squeeze()

    print(pred_y)

# train_classifer()
predict()

