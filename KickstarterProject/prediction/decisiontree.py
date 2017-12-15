from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

# x = [[0, 0], [1, 1]]
# y = [0, 1]
x = pd.read_csv('train.csv', dtype = float, usecols=['goal','period','subcategory_rate','state_rate','creator_rate'])
y = pd.read_csv('train.csv', dtype = float, usecols=['state'])

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.33,
                                                    random_state=0,
                                                    stratify=y)

x = x_train.values
x = np.ndarray.tolist(x)
y = y_train.values
y = np.ndarray.tolist(y)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
# save data
joblib.dump(clf, "decision_tree.m")

prediction =  clf.predict(x_test)
np_prediction = np.array(prediction).reshape((len(prediction), 1))
np_y = np.array(y_test)

print(np_prediction.shape)
print(np_y.shape)
print(np_prediction)
print(np_y)

res = np_prediction - np_y
print(np.sum(np.abs(res))/len(res))