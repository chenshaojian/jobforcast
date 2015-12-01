# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
import xgboost as xgb
import numpy as np

# handle train data
x,ydegree,ysize,ysalary,yposition,x_train,x_valid,x_test,y_train,y_valid,test_id=[],[],[],[],[],[],[],[],[],[],[]
fin,fin2=open("../out/train"+VERSION+".csv"),open("../out/test"+VERSION+".csv")
fin.readline()
for line in fin:
    fields=line.split(",")
    # remove train id and label
    x.append(map(float,fields[1:-4]))
    # split 4 kinds of labels
    ydegree.append(float(fields[-4]))
    ysize.append(float(fields[-3]))
    ysalary.append(float(fields[-2]))
    yposition.append(float(fields[-1]))
fin.close()

# handle valid data
x_train, x_valid, ydegree_train, ydegree_valid, ysize_train, ysize_valid, ysalary_train, ysalary_valid,\
yposition_train, yposition_valid = train_test_split(x, ydegree, ysize, ysalary, yposition, test_size=0.33, random_state=RANDSEED)

# handle test data
fin2.readline()
for line in fin2:
    fields=line.split(",")
    test_id.append(fields[0])
    # remove test id
    x_test.append(map(float,fields[1:]))
fin2.close()

# data
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
degree_ac=accuracy_score(ydegree_valid, degree_model.predict(xg_valid))

xg_train=xgb.DMatrix(x_train, label=ysize_train)
xg_valid=xgb.DMatrix(x_valid, label=ysize_valid)
xg_train_online=xgb.DMatrix(x, label=ysize)
param['num_class']=8
watchlist=[(xg_train,'train'),(xg_valid,'valid')]

size_model=xgb.train(param, xg_train, num_round, watchlist);
size_ac=accuracy_score(ysize_valid, size_model.predict(xg_valid))

xg_train=xgb.DMatrix(x_train, label=ysalary_train)
xg_valid=xgb.DMatrix(x_valid, label=ysalary_valid)
xg_train_online=xgb.DMatrix(x, label=ysalary)
param['num_class']=7
watchlist=[(xg_train,'train'),(xg_valid,'valid')]

salary_model=xgb.train(param, xg_train, num_round, watchlist);
salary_ac=accuracy_score(ysalary_valid, salary_model.predict(xg_valid))

xg_train=xgb.DMatrix(x_train, label=yposition_train)
xg_valid=xgb.DMatrix(x_valid, label=yposition_valid)
xg_train_online=xgb.DMatrix(x, label=yposition)
param['num_class']=33
watchlist=[(xg_train,'train'),(xg_valid,'valid')]

position_model=xgb.train(param, xg_train, num_round, watchlist);
position_ac=accuracy_score(yposition_valid, position_model.predict(xg_valid))

print degree_ac,size_ac,salary_ac,position_ac

# best: 0.656994818653 0.414196891192 0.596373056995 0.530466321244, online score: 0.50951
# xgboost: 0.652632657242 0.376357303831 0.569350542922 0.562077443147, online score: 0.49258

# predict
xg_train_online=xgb.DMatrix(x, label=ydegree)
param['num_class']=3
degree_model=xgb.train(param, xg_train_online, num_round);

xg_train_online=xgb.DMatrix(x, label=ysize)
param['num_class']=8
size_model=xgb.train(param, xg_train_online, num_round);

xg_train_online=xgb.DMatrix(x, label=ysalary)
param['num_class']=7
salary_model=xgb.train(param, xg_train_online, num_round);

xg_train_online=xgb.DMatrix(x, label=yposition)
param['num_class']=33
position_model=xgb.train(param, xg_train_online, num_round);

print "start predicting..."
fout=open("../out/result"+VERSION+".csv","w")
fout.write("id,degree,size,salary,position_name\n")
ydegree_test=degree_model.predict(xg_test_online)
ysize_test=size_model.predict(xg_test_online)
ysalary_test=salary_model.predict(xg_test_online)
yposition_test=position_model.predict(xg_test_online)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outlist=[test_id[i],str(int(ydegree_test[i])),str(int(ysize_test[i])),str(int(ysalary_test[i])),position_map2[int(yposition_test[i])]]
    fout.write(",".join(outlist)+"\n")
fout.close()