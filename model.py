import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from sklearn.svm import svmodel
import numpy as np

data = pd.read_csv("Door_csv.csv")

#expanding dataset for better training
data_expand_pos = data.copy()
data_expand_pos[['GY', 'AZ']] += 0.01

data_expand_neg = data.copy()
data_expand_neg[['GY','AZ']] -= 0.01

#Concatenating expanded data with original data
data_expanded = pd.concat([data, data_expand_pos, data_expand_neg])
data_expanded.to_csv(fdir+"final_input.csv")

#Splitting input data file into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(data_expanded[['GY','AZ']], data_expanded['STATE'], test_size=0.2)

#training the model and getting accuracy on test set
svm = svmodel(kernel = 'linear')
svm.fit(x_train, y_train)
y_pred = svm.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"SVM Accuracy is:{accuracy}")

with open(fdir+"svm.pkl", "wb") as f:
    pickle.dump(svm, f)

with open(fdir+"svm.pkl", "rb") as f:
    svm_ = pickle.load(f)