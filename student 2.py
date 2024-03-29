# -*- coding: utf-8 -*-
"""Naive_Bayes1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SmGR8UCxjK905aTb4TpDAgHTO0A5ohmX
"""

import sys
import numpy as np
import pandas as pd
import csv

def calculate_prior(df, Y):
    classes = sorted(list(df[Y].unique()))
    prior = []
    for i in classes:
        prior.append(len(df[df[Y]==i])/len(df))
    return prior

def naive_bayes_gaussian(df, X, Y):
    
    features = list(df.columns)[1:3]

 
    prior = calculate_prior(df, Y)

    Y_pred = []
    
    for x in X:
        
        labels = sorted(list(df[Y].unique()))
        likelihood = [1]*len(labels)
        for j in range(len(labels)):
            for i in range(len(features)):
                likelihood[j] *= calculate_likelihood_gaussian(df, features[i], x[i], Y, labels[j])

       
        post_prob = [1]*len(labels)
        for j in range(len(labels)):
            post_prob[j] = likelihood[j] * prior[j]

        Y_pred.append(np.argmax(post_prob))

    return np.array(Y_pred)

def calculate_likelihood_gaussian(df, feat_name, feat_val, Y, label):
    feat = list(df.columns)
    df = df[df[Y]==label]
    mean, std = df[feat_name].mean(), df[feat_name].std()
    #print(mean)
    #print(std)
    p_x_given_y = (1 / (np.sqrt(2 * np.pi) * std)) *  np.exp(-((feat_val-mean)**2 / (2 * std**2 )))
    return p_x_given_y

if __name__ == "__main__":
    expected_args = ["--data"]
    arg_len = len(sys.argv)
    info = []

    for i in range(len(expected_args)):
        for j in range(1, len(sys.argv)):
            if expected_args[i] == sys.argv[j] and sys.argv[j + 1]:
                info.append(sys.argv[j + 1])
    
    data = pd.read_csv(info[0], header=None)

    X_test = data.iloc[:,1:3].values
    Y_test = data.iloc[:,:1].values
    Y_pred = naive_bayes_gaussian(data, X=X_test, Y=0)
    cnt = 0
    for i in range(0,len(Y_pred)):
     if(Y_pred[i])==0:
       if(Y_test[i]=="B"):
         cnt+=1
     if(Y_pred[i])==1:
       if(Y_test[i]=="A"):
         cnt+=1
    Y_2=np.array(data.iloc[:,:1])
    X_2=np.array(data.iloc[:,1:2])
    X_3=np.array(data.iloc[:,2:3])
    X_2_meanstd_A = []
    X_3_meanstd_A = []
    X_2_meanstd_B = []
    X_3_meanstd_B = []
    for i in range(0,len(Y_2)):
     if(Y_2[i])=="A":
       X_2_meanstd_A.append(X_2[i])
       X_3_meanstd_A.append(X_3[i])
     elif(Y_2[i])=="B":
       X_2_meanstd_B.append(X_2[i])
       X_3_meanstd_B.append(X_3[i]) 
    a= calculate_prior(data, 0)
    def var(numbers, mean_num):
      avg = mean_num
      variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
      return variance
    X_2_std_A = var(X_2_meanstd_A,np.mean(X_2_meanstd_A))
    X_3_std_A = var(X_3_meanstd_A,np.mean(X_3_meanstd_A))
    X_2_std_B = var(X_2_meanstd_B,np.mean(X_2_meanstd_B))
    X_3_std_B = var(X_3_meanstd_B,np.mean(X_3_meanstd_B))
    print(np.mean(X_2_meanstd_A),  *X_2_std_A, np.mean(X_3_meanstd_A), *X_3_std_A, a[0], sep=",")
    print(np.mean(X_2_meanstd_B),  *X_2_std_B, np.mean(X_3_meanstd_B), *X_3_std_B, a[1], sep=",")
    print(cnt)