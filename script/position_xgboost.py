# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
import xgboost as xgb
import numpy as np

# 1.0.568018848597
# 2.0.563306699447

# handle train data
x,yposition,x_train,x_valid,x_test,test_id=[],[],[],[],[],[]
ftrainposition,ftestposition=open("../out/train_position_"+VERSION+".csv"),open("../out/test_position_"+VERSION+".csv")
ftrainposition.readline()
for line in ftrainposition:
    fields=line.split(",")
    # remove train id and label
    x.append(map(float,fields[1:-1]))
    yposition.append(float(fields[-1]))
ftrainposition.close()

# handle valid data
x_train, x_valid, yposition_train, yposition_valid = train_test_split(x, yposition, test_size=0.33, random_state=RANDSEED)

# handle test data
ftestposition.readline()
for line in ftestposition:
    fields=line.split(",")
    test_id.append(fields[0])
    # remove test id
    x_test.append(map(float,fields[1:]))
ftestposition.close()

# data
print "make data..."
xg_train=xgb.DMatrix(x_train, label=yposition_train)
xg_valid=xgb.DMatrix(x_valid, label=yposition_valid)
xg_train_online=xgb.DMatrix(x, label=yposition)
xg_test_online=xgb.DMatrix(x_test)
param={}
param['objective']='multi:softmax'
param['eta']=0.1
param['max_depth']=6
param['silent']=1
param['nthread']=4
param['num_class']=33
watchlist=[(xg_train,'train'),(xg_valid,'valid')]
num_round=5

# train
print "start training...",len(x_train)
position_model=xgb.train(param, xg_train, num_round, watchlist);

# evaluate
print "start evaluating...",len(x_valid)
position_ac=accuracy_score(yposition_valid, position_model.predict(xg_valid))
print position_ac

# predict
print "start build position model..."
position_model=xgb.train(param, xg_train_online, num_round, watchlist);

print "start predicting..."
foutposition=open("../out/result_position_"+VERSION+".csv","w")
foutposition.write("id,position\n")
yposition_test=position_model.predict(xg_test_online)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outposition=[test_id[i],position_map2[int(yposition_test[i])]]
    foutposition.write(",".join(outposition)+"\n")
foutposition.close()