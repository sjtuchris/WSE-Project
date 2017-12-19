from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

import torch
import torch.nn.functional as F  
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


class Net(torch.nn.Module):  
    def __init__(self, n_feature, n_hidden1, n_hidden2, n_output):
        super(Net, self).__init__()  
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden1)  # Output of hidden layer
        self.hidden2 = torch.nn.Linear(n_hidden1, n_hidden2)
        self.predict = torch.nn.Linear(n_hidden2, n_output)  # Output of prediction layer

    def forward(self, x):  
        x = F.relu(self.hidden1(x))  # Activation Function
        x = F.relu(self.hidden2(x))
        x = self.predict(x)  # Prediction
        return x


net = Net(n_feature=5, n_hidden1=20, n_hidden2=20, n_output=1)

# optimizer is the training tool
optimizer = torch.optim.SGD(net.parameters(), lr=0.05)  # input training features and learning rate
loss_func = torch.nn.MSELoss()  # Mean square error

for t in range(300):
    prediction = net(x)  # feeding training data to the model

    # print(prediction.data)

    loss = loss_func(prediction, y)  # calculate error
    print(loss.data[0])

    optimizer.zero_grad()  
    loss.backward()  # Back propagation
    optimizer.step()  # Update parameters

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