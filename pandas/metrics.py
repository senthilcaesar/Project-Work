# Calculate different model performance metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 400

df = pd.read_csv('Chapter_1_cleaned_data.csv')

from sklearn.model_selection import train_test_split

x = df['EDUCATION'].values.reshape(-1,1)
y = df['default payment next month'].values

X_train, X_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.2,
                                                    random_state=24)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn.linear_model import LogisticRegression
example_lr = LogisticRegression()
example_lr.fit(X_train, y_train)
y_pred = example_lr.predict(X_test)

''' How should we assess the accuracy of the prediction ? '''
from sklearn import metrics
print(metrics.accuracy_score(y_test, y_pred))
print(metrics.confusion_matrix(y_test, y_pred))

'''Obtaining predicted probabilities'''
y_pred_prob = example_lr.predict_proba(X_test)
# Probabilities over the class add up to 1
prob_sum = np.sum(y_pred_prob, 1)
print(y_pred_prob)

pos_prob = y_pred_prob[:,1]
fpr, tpr, thresholds = metrics.roc_curve(y_test, pos_prob)
plt.plot(fpr, tpr, '*-')
plt.plot([0,1], [0,1], 'r--')
plt.legend(['Logistic regression', 'Random chance'])
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC curve')

# Calculate the area under the ROC curve
print(metrics.roc_auc_score(y_test, pos_prob))
