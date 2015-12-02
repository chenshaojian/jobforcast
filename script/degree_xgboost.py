# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
import xgboost as xgb
import numpy as np

# 1.0.645666871543
# 2.0.614730587994
# 3.0.645974185618
# 4.0.635115754968 new feature

# handle train data
x,ydegree,x_train,x_valid,x_test,test_id=[],[],[],[],[],[]
ftraindegree,ftestdegree=open("../out/train_degree_"+VERSION+".csv"),open("../out/test_degree_"+VERSION+".csv")
ftraindegree.readline()
for line in ftraindegree:
    fields=line.split(",")
    # remove train id and label
    x.append(map(float,fields[1:-1]))
    ydegree.append(float(fields[-1]))
ftraindegree.close()

# handle valid data
x_train, x_valid, ydegree_train, ydegree_valid = train_test_split(x, ydegree, test_size=0.33, random_state=RANDSEED)

# handle test data
ftestdegree.readline()
for line in ftestdegree:
    fields=line.split(",")
    test_id.append(fields[0])
    # remove test id
    x_test.append(map(float,fields[1:]))
ftestdegree.close()

# data
print "make data..."
xg_train=xgb.DMatrix(x_train, label=ydegree_train)
xg_valid=xgb.DMatrix(x_valid, label=ydegree_valid)
xg_train_online=xgb.DMatrix(x, label=ydegree)
xg_test_online=xgb.DMatrix(x_test)
param={}
param['objective']='multi:softmax'
param['eta']=0.1
param['max_depth']=6
param['silent']=1
param['nthread']=3
param['num_class']=3
watchlist=[(xg_train,'train'),(xg_valid,'valid')]
num_round=1000

# train
print "start training...",len(x_train)
degree_model=xgb.train(param, xg_train, num_round, watchlist);

# evaluate
print "start evaluating...",len(x_valid)
degree_ac=accuracy_score(ydegree_valid, degree_model.predict(xg_valid))
print degree_ac

# predict
print "start build degree model..."
degree_model=xgb.train(param, xg_train_online, num_round);

print "start predicting..."
foutdegree=open("../out/result_degree_"+VERSION+".csv","w")
foutdegree.write("id,degree\n")
ydegree_test=degree_model.predict(xg_test_online)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outdegree=[test_id[i],str(int(ydegree_test[i]))]
    foutdegree.write(",".join(outdegree)+"\n")
foutdegree.close()