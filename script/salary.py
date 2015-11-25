# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

# handle train data
x,ysalary,x_train,x_valid,x_test,test_id=[],[],[],[],[],[]
ftrainsalary,ftestsalary=open("../out/train_salary_"+VERSION+".csv"),open("../out/test_salary_"+VERSION+".csv")
ftrainsalary.readline()
for line in ftrainsalary:
    fields=line.split(",")
    # remove train id and label
    x.append(map(float,fields[1:-1]))
    ysalary.append(float(fields[-1]))
ftrainsalary.close()

# handle valid data
x_train, x_valid, ysalary_train, ysalary_valid = train_test_split(x, ysalary, test_size=0.33, random_state=RANDSEED)

# handle test data
ftestsalary.readline()
for line in ftestsalary:
    fields=line.split(",")
    test_id.append(fields[0])
    # remove test id
    x_test.append(map(float,fields[1:]))
ftestsalary.close()

# train
print "start training...",len(x_train)
salary_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, ysalary_train)
print "salary feature:",salary_model.feature_importances_

# evaluate
print "start evaluating...",len(x_valid)
salary_ac=accuracy_score(ysalary_valid, salary_model.predict(x_valid))
print salary_ac

# predict
print "start build salary model..."
salary_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, ysalary)

print "start predicting..."
foutsalary=open("../out/result_salary_"+VERSION+".csv","w")
foutsalary.write("id,salary\n")
ysalary_test=salary_model.predict(x_test)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outsalary=[test_id[i],str(int(ysalary_test[i]))]
    foutsalary.write(",".join(outsalary)+"\n")
foutsalary.close()