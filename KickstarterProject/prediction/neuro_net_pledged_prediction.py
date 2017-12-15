from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

import torch
import torch.nn.functional as F  # 激励函数都在这
from torch.autograd import Variable

import matplotlib.pyplot as plt

x = pd.read_csv('train.csv', dtype=float, usecols=['goal','period','subcategory_rate','state_rate','creator_rate'])
# add feature
# 1. blurb len
# 2. success rate of category
# 3. success rate of state in US
# 4. goal
# 5. period
# 6. creator

y = pd.read_csv('train.csv', dtype=float, usecols=['pledged'])
x = x.values

x = np.ndarray.tolist(x)
# normalization
x = preprocessing.scale(x)
x = np.array(x)
np_x = x.astype(float)

y = y.values.reshape((len(y), 1)).astype(float)
np_y = y / 10000

# y = np.ndarray.tolist(y)
# print(x.shape)
# print(y.shape)

x = torch.from_numpy(np_x).float()
y = torch.from_numpy(np_y).float()

# x = torch.unsqueeze(torch.linspace(-1, 1, 100), dim=1)  # x data (tensor), shape=(100, 1)
# y = x.pow(2) + 0.2*torch.rand(x.size())                 # noisy y data (tensor), shape=(100, 1)

x, y = torch.autograd.Variable(x), Variable(y)


class Net(torch.nn.Module):  # 继承 torch 的 Module
    def __init__(self, n_feature, n_hidden1, n_hidden2, n_output):
        super(Net, self).__init__()  # 继承 __init__ 功能
        # 定义每层用什么样的形式
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden1)  # 隐藏层线性输出
        self.hidden2 = torch.nn.Linear(n_hidden1, n_hidden2)
        self.predict = torch.nn.Linear(n_hidden2, n_output)  # 输出层线性输出

    def forward(self, x):  # 这同时也是 Module 中的 forward 功能
        # 正向传播输入值, 神经网络分析出输出值
        x = F.relu(self.hidden1(x))  # 激励函数(隐藏层的线性值)
        x = F.relu(self.hidden2(x))
        x = self.predict(x)  # 输出值
        return x


net = Net(n_feature=5, n_hidden1=20, n_hidden2=20, n_output=1)

# optimizer 是训练的工具
optimizer = torch.optim.SGD(net.parameters(), lr=0.05)  # 传入 net 的所有参数, 学习率
loss_func = torch.nn.MSELoss()  # 预测值和真实值的误差计算公式 (均方差)

for t in range(300):
    prediction = net(x)  # 喂给 net 训练数据 x, 输出预测值

    # print(prediction.data)

    loss = loss_func(prediction, y)  # 计算两者的误差
    print(loss.data[0])

    optimizer.zero_grad()  # 清空上一步的残余更新参数值
    loss.backward()  # 误差反向传播, 计算参数更新值
    optimizer.step()  # 将参数更新值施加到 net 的 parameters 上

torch.save(net, "neuro_net_pledge.pkl")
net2 = torch.load("neuro_net_pledge.pkl")
prediction = net2(x)
#
# prediction = net(x)
# print(prediction.data.numpy())
# print(y.data.numpy())
# print(sum(abs(prediction.data.numpy() - y.data.numpy())) / len(y.data.numpy()))

# plot on two dimention
axes = plt.gca()
axes.set_ylim([0, 500])
plt.scatter(np_x[:, 4], np_y,label='traning', alpha=0.2)
plt.scatter(np_x[:, 4], prediction.data.numpy(),label='regression', alpha=0.2)
plt.legend(loc='upper right')

# fig = plt.figure()
# ax = Axes3D(fig)
plt.show()