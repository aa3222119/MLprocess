#!/usr/bin/env python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import  train_test_split,cross_val_score
from sklearn.decomposition import PCA
import time
import datetime
import numpy as np
#read train data
data=pd.read_csv('C:\\Users\\Administrator\\Downloads\\train2.csv')
#delete useless columns
del_columns=['product_desc','domain','city_code','sub_town_code','user_state_codeset']
for d in del_columns:
    data.drop(labels=d,axis=1,inplace=True)


#detele Ambiguous data to ensure the accuracy of model
data.drop(data[(data['sex']=='0')|(data['sex']=='1')].index,inplace=True)
print(data.shape)

gprs=['from_0_to_6_gprs','from_6_to_7_gprs','from_7_to_8_gprs','from_8_to_9_gprs','from_9_to_12_gprs','from_12_to_18_gprs','from_18_to_19_gprs','from_19_to_22_gprs'
      ,'from_22_to_23_gprs','from_23_to_24_gprs','from_0_to_6_times','from_6_to_7_times','from_7_to_8_times','from_8_to_9_times','from_9_to_12_times','from_12_to_18_times','from_18_to_19_times'
      ,'from_19_to_22_times','from_22_to_23_times','from_23_to_24_times']
for i in gprs:
    data[i]=data[i].fillna(0)
#print(data.isnull().sum())
data['last_stop_time']=data['last_stop_time'].fillna(19900101000000)

#fillna
numeric_fea=data.dtypes[data.dtypes!="object"].index
categories_fea=data.dtypes[data.dtypes=="object"].index
for n in numeric_fea:
    data[n]=data[n].fillna(0)

for c in categories_fea:
    data[c]=data[c].fillna("Missing")

#delete columns where the values all null or in the same values
data_columns=data.columns
for i in data_columns:
    c=pd.value_counts(data[i])
    c_t=c.shape
    if c_t[0]==1:
        data.drop(labels=i,axis=1,inplace=True)
#a=data.ix[:,(data != data.ix[0]).any()]
print(data.is_away.value_counts())
data['last_stop_time']=data['last_stop_time'].replace('(null)',value=19900101000000)
data['sex']=data['sex'].replace({'F':0,'M':1})
data['brand_code']=data['brand_code'].replace({'G001':1,'G002':2,'G004':3,'G005':4,'G010':5,'Missing':0})
#data['job_type_code']=data['job_type_code'].replace({'Missing':10,'A':1})
#data['last_stop_time']=data['last_stop_time'].astype(str)

"""
data=data.replace({"sex":{'F':0,'M':1},
                   "brand_code":{'G001':1,'G002':2,'G004':3,'G005':4,'G010':5,'Missing':0},
                   "job_type_code":{'Missing':10,'A':1},
                   "last_stop_time": {'(null)': 19900101000000}
                   })
"""
#print(data.sex.value_counts())
#print(data.job_type_code.value_counts())
#print(data.last_stop_time.value_counts())
#calculate the gap of the time between now
#test=(datetime.datetime.now()-datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(data['last_stop_time'][1]), '%Y%m%d%H%M%S')))).days
data['last_stop_time']=data['last_stop_time'].map(lambda x:(datetime.datetime.now()-datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(x), '%Y%m%d%H%M%S')))).days)
data['last_stop_time']=data['last_stop_time'].astype(int)
#print((datetime.datetime.now()-test).days)
#print(data.last_time.value_counts())
categories=data.dtypes[data.dtypes=='object'].index
print(categories)

for i in categories:
    for_dummy=data.pop(i)
    extra_data=pd.get_dummies(for_dummy,prefix=i)
    data=pd.concat([data,extra_data],axis=1)






X=data.drop(labels='is_away',axis=1)
Y=data['is_away']

#using PCA for dimensionality reduction
#pca=PCA()
#x_pca=pca.fit_transform(X)


print('start split data')
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3,random_state=0)
print('split data successful')
print(y_train.value_counts())
s=StandardScaler()
#print(x_train.describe)
print('start fit features')
s.fit(x_train)
print('fit finished')
x_train_standard=s.transform(x_train)
x_test_standard=s.transform(x_test)

print('start modeling')
LR=LogisticRegression(C=10000)
LR.fit(x_train,y_train)
print('modeling finished')
y_pre=LR.predict(x_test)

y_prob=LR.predict_proba(x_test_standard)

accuracy_=LR.score(x_test_standard,y_test)
print("the accuracy is :{}".format(accuracy_))

def accuracy(x,y):
    count=0
    for i,predictions in enumerate(y):
        if x.iloc[i]==predictions:
            count+=1

    return count/len(x)

score=cross_val_score(LR,x_test,y_test)
print("准确率 :{}".format(np.mean(score)))
print("精确度：{}".format(accuracy(y_test,y_pre)))
for i, predictions in enumerate(y_pre[-15:]):
    print('预测结果：%s. 信息: %s' % (predictions, y_test.iloc[i]))


