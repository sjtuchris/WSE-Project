from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.externals import joblib

# x = [[0, 0], [1, 1]]
# y = [0, 1]
x = pd.read_csv('new.csv', dtype = float, usecols=['backers_count','comment_num','goal','period','pledged','update'])
y = pd.read_csv('new.csv', dtype = float, usecols=['state'])
x = x.values
x = np.ndarray.tolist(x)
y = y.values
y = np.ndarray.tolist(y)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
# save data
joblib.dump(clf, "decision_tree.m")

prediction =  clf.predict(x)
np_prediction = np.array(prediction).reshape((len(prediction), 1))
np_y = np.array(y)

print(np_prediction.shape)
print(np_y.shape)
print(np_prediction)
print(np_y)

res = np_prediction - np_y
print(np.sum(np.abs(res)))