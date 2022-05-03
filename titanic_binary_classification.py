# -*- coding: utf-8 -*-
"""titanic_binary_classification

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H-YvHn1eL2gHlABm6AmuBMGuK6BaR63i
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

titanic=pd.read_csv('/content/drive/MyDrive/train.csv')
titanic

#Count the number of rows and colums in dataset
titanic.shape

#get some statistics
titanic.describe()

#get a count of number of survivors
titanic['Survived'].value_counts()

#visualize the count of survivors
sns.countplot(titanic['Survived'])

#visualize the count of survivors for colums 'who', 'sex','pclass','sibsp','parch','embarked'

cols=['Sex','Pclass','SibSp','Parch','Embarked']

n_rows=2
n_cols=3

#the subplot grid and figure size of each graph
fig, axs=plt.subplots(n_rows, n_cols, figsize=(n_cols*3.2, n_rows*3.2))

for r in range(0,n_rows):
  for c in range(0,n_cols):
    i=r*n_cols+c #index to go through the number of columns
    ax=axs[r][c] #show where to position each subplot
    sns.countplot(titanic[cols[i]],hue=titanic['Survived'],ax=ax)
    ax.set_title(cols[i])
    ax.legend(title='survived',loc='upper right')

plt.tight_layout()

# sns.countplot(titanic['Sex'],titanic['Survived'])

#look at the survival rate by sex
titanic.groupby('Sex')[['Survived']].mean()

#look at the survival rate by class
#titanic.groupby('Pclass')[['Survived']].mean()



#look at the survival rate by class
titanic.groupby('Pclass')[['Survived']].mean()

#look at the pivot table by sex and class
#titanic.pivot_table('Survived',index='Sex',columns='Pclass')


#look at the pivot table by sex and class
titanic.pivot_table('Survived',index='Pclass',columns='Sex')

#look at the survival rate by sex and class visually
#titanic.pivot_table('Survived',index='Sex',columns='Pclass').plot()


titanic.pivot_table('Survived',index='Pclass',columns='Sex').plot()

#plot the survival rate of each class
#sns.barplot(x='Pclass',y='Survived',data=titanic)


#plot the survival rate of each class
sns.barplot(x='Pclass',y='Survived',data=titanic)

#Look at the survival rate by sex,age and class
age=pd.cut(titanic['Age'],[0,18,80])
titanic.pivot_table('Survived',['Sex','Age'],'Pclass')

#Plot the prices paid of each class
plt.scatter(titanic['Fare'],titanic['Pclass'],color='purple',label='Passenger Paid')
plt.ylabel('Class')
plt.xlabel('Price/Fare')
plt.title('Price of Each Class')
plt.legend()
plt.show()

#Count the empty values in each column
titanic.isna().sum()

#Look at all of the values ineach colunn and get a count
for val in titanic:
  print(titanic[val].value_counts())

# #Drop the columns
titanic=titanic.drop(['PassengerId','Name','Ticket','Cabin'],axis=1)

#remove the rpws with missing values
titanic=titanic.dropna(subset=['Embarked','Age'])

#Count the new number of rows and columns in the dataset
titanic.shape

#Look at the datatypes
titanic.dtypes

#print the unique values and columns
print(titanic['Sex'].unique())

print(titanic['Embarked'].unique())

# from sklearn import preprocessing

#

from sklearn import preprocessing
labelEncoder=preprocessing.LabelEncoder()

#Encode the sex column
titanic.iloc[:, 2]=labelEncoder.fit_transform(titanic.iloc[:, 2].values)


#Encode the embarked column
titanic.iloc[:, 7]=labelEncoder.fit_transform(titanic.iloc[:, 7].values)

print(titanic['Sex'].unique())

print(titanic['Embarked'].unique())

titanic.dtypes

titanic

#Split the data into independent 'X' and depemdent 'Y' variables
X=titanic.iloc[:,1:8].values
Y=titanic.iloc[:,0].values

#Split the dataset into 80%training and 20% testing
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=0)

#Scale the data
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.fit_transform(X_test)

#Create a function with many machine learning models
def models(X_train,Y_train):
  #use logistic regression
  from sklearn.linear_model import LogisticRegression
  log=LogisticRegression(random_state=0)
  log.fit(X_train,Y_train)

  #Use Kneighbors
  from sklearn.neighbors import KNeighborsClassifier
  knn=KNeighborsClassifier(n_neighbors=5,metric='minkowski',p=2)
  knn.fit(X_train,Y_train)

  #Use SVC(linear kernel)
  from sklearn.svm import SVC
  svc_lin=SVC(kernel='linear',random_state=0)
  svc_lin.fit(X_train,Y_train)

  #Use SVC(RBF kernel)
  from sklearn.svm import SVC
  svc_rbf=SVC(kernel='rbf',random_state=0)
  svc_rbf.fit(X_train,Y_train)

  #Use GaussianNB
  from sklearn.naive_bayes import GaussianNB
  gauss=GaussianNB()
  gauss.fit(X_train,Y_train)

  #Use decision tree
  from sklearn.tree import DecisionTreeClassifier
  tree=DecisionTreeClassifier(criterion='entropy',random_state=0)
  tree.fit(X_train,Y_train)

  #use randomForestClassifier
  from sklearn.ensemble import RandomForestClassifier
  forest=RandomForestClassifier(n_estimators=10,criterion='entropy',random_state=0)
  forest.fit(X_train,Y_train)

  #Print the training accuracy
  print('[0]Logistic Regression Training accuracy',log.score(X_train,Y_train))
  print('[1]K Neighbors Training accuracy',knn.score(X_train,Y_train))
  print('[2]SVC Linear Training accuracy',svc_lin.score(X_train,Y_train))
  print('[3]SVC rbf Training accuracy',svc_rbf.score(X_train,Y_train))
  print('[4]GAussian NB Training accuracy',gauss.score(X_train,Y_train))
  print('[5]Decision Tree Training accuracy',tree.score(X_train,Y_train))
  print('[6]random Forest Training accuracy',forest.score(X_train,Y_train))

  return log,knn,svc_lin,svc_rbf,gauss,tree,forest

#get and train all the models
model=models(X_train,Y_train)

#Show the confusion matrix and accuracy for all the models on test data
from sklearn.metrics import confusion_matrix

for i in range(len(model)):
  cm=confusion_matrix(Y_test,model[i].predict(X_test))

  #Extract the true negtive, False positive , false negative, true positive
  TN,FP,FN,TP=confusion_matrix(Y_test,model[i].predict(X_test)).ravel()

  test_score=(TP+TN)/(TP+TN+FN+FP)

  print(cm)
  print('Model[{}] Testing Accuracy = "{}"'.format(i, test_score))
  print()

#Get feature importance
forest=model[6]
importances=pd.DataFrame({'feature':titanic.iloc[:,1:8].columns, 'importance':np.round(forest.feature_importances_,3)})
importances=importances.sort_values('importance',ascending=False).set_index('feature')
importances

#Visualize the importance
importances.plot.bar()

#print the prediction of the random forest classifier 
pred=model[6].predict(X_test)
print(pred)

print()

#print the actual values
print(Y_test)

# # Pclass        int64
# # Sex           int64
# # Age         float64
# # SibSp         int64
# # Parch         int64
# # Fare        float64
# # Embarked      int64


# my_survival=[[1,0,29,10,10,300,3]]

# #scaling my survival
# from sklearn.preprocessing import StandardScaler
# sc=StandardScaler()
# X_train=sc.transform(X_train)

# my_survival_scaled=sc.transform(my_survival)


# #print prediction of my survival using random forest classifier
# pred=model[6].predict(my_survival_scaled)
# print(pred)

# if pred==0:
#   print('You did not survive')
# else:
#   print('You survived!')

# my_survival = [[3, 1, 80, 0, 0, 15, 1 ]]

# #print prediction
# pred = model[6].predict(my_survival)
# print(pred)

# if pred == 0:
#   print("Ohn you didnt survive!!")
# else:
#   print('Congrats you made it!')

X1=np.array([3, 1, 5, 0, 0, 100, 0])

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
my_survival=sc.fit_transform(X1[:, np.newaxis])
print(my_survival)
my_survival=my_survival.transpose()
print(my_survival)
pred= model[6].predict(my_survival)
print(pred)

#
if pred== 0:
  print("oh well, you died!")
else:
  print("You lucky! you saved!")