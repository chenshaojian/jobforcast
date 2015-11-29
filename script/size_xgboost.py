# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
import xgboost as xgb
import numpy as np

# 1.0.404322884655
# 2.0.39377176808
# 3.0.369289080107

# handle train data
x,ysize,x_train,x_valid,x_test,test_id=[],[],[],[],[],[]
ftrainsize,ftestsize=open("../out/train_size_"+VERSION+".csv"),open("../out/test_size_"+VERSION+".csv")
ftrainsize.readline()
for line in ftrainsize:
    fields=line.split(",")
    # remove train id and label
    x.append(map(float,fields[1:-1]))
    ysize.append(float(fields[-1]))
ftrainsize.close()

# handle valid data
x_train, x_valid, ysize_train, ysize_valid = train_test_split(x, ysize, test_size=0.33, random_state=RANDSEED)

# handle test data
ftestsize.readline()
for line in ftestsize:
    fields=line.split(",")
    test_id.append(fields[0])
    # remove test id
    x_test.append(map(float,fields[1:]))
ftestsize.close()

# data
print "make data..."
xg_train=xgb.DMatrix(x_train, label=ysize_train)
xg_valid=xgb.DMatrix(x_valid, label=ysize_valid)
xg_train_online=xgb.DMatrix(x, label=ysize)
xg_test_online=xgb.DMatrix(x_test)
param={}
param['objective']='multi:softmax'
param['eta']=0.1
param['max_depth']=6
param['silent']=1
param['nthread']=4
param['num_class']=8
watchlist=[(xg_train,'train'),(xg_valid,'valid')]
num_round=1000

# train
print "start training...",len(x_train)
size_model=xgb.train(param, xg_train, num_round, watchlist);

# evaluate
print "start evaluating...",len(x_valid)
size_ac=accuracy_score(ysize_valid, size_model.predict(xg_valid))
print size_ac

# predict
print "start build size model..."
size_model=xgb.train(param, xg_train_online, num_round);

print "start predicting..."
foutsize=open("../out/result_size_"+VERSION+".csv","w")
foutsize.write("id,size\n")
ysize_test=size_model.predict(xg_test_online)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outsize=[test_id[i],str(int(ysize_test[i]))]
    foutsize.write(",".join(outsize)+"\n")
foutsize.close()