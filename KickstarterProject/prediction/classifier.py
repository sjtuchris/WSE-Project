from __future__ import print_function, division
import os
import torch
import pandas as pd
import numpy as np
import torch.nn.functional as F     
import matplotlib.pyplot as plt
import torch.utils.data as Data
from torchvision import transforms, utils
from torch.autograd import Variable 
from sklearn import preprocessing



# # Ignore warnings
# import warnings
# warnings.filterwarnings("ignore")

class Net(torch.nn.Module):     
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.out = torch.nn.Linear(n_hidden, n_output)    

    def forward(self, x):
        x = F.relu(self.hidden(x))   
        x = self.out(x)              
        return x

def train_classifer():
    net = Net(n_feature=5, n_hidden=10, n_output=2)

    features_set = pd.read_csv('train.csv', dtype = float, usecols=['goal','period','subcategory_rate','state_rate','creator_rate'])

    results_set = pd.read_csv('train.csv', usecols=['state'])

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

    optimizer = torch.optim.SGD(net.parameters(), lr=0.1) 
    loss_func = torch.nn.CrossEntropyLoss()

    for epoch in range(3):
        for step, (batch_x, batch_y) in enumerate(loader):
            out = net(Variable(batch_x))     

            loss = loss_func(out, Variable(batch_y))

            optimizer.zero_grad() 
            loss.backward()       
            optimizer.step()      

            print('Epoch: ', epoch, '| Step: ', step, '| batch x: ',
              batch_x.numpy(), '| batch y: ', batch_y.numpy())

    out = net(features)
    prediction = torch.max(F.softmax(out), 1)[1]
    pred_y = prediction.data.numpy().squeeze()
    print(sum(abs(pred_y-results_set.values.flatten()))/len(pred_y))
    torch.save(net.state_dict(), "net")

def predict():
    net = Net(n_feature=5, n_hidden=10, n_output=2)
    net.load_state_dict(torch.load("net"))
    features_set = [10000,3,0.6,0.5,0.7]
    # features_set = [[4,0,30000,0,28,56],[648,68,11000,16,31,24000],[4,0,30000,0,28,56],[0,0,3500,0,60,0]]
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

train_classifer()
predict()