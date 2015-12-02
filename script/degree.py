# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

# 1.0.640954722393
# 2.0.635525507068 remove posset,indusset,maxposlevel
# 3.0.641979102643 add first,last,next industry
# 4.0.646588813768 add first-last,first-next indus,size,salary,pos,poslevel,firstposlevel,firstposition
# 5.0.662671583692 merge to one feature list
# 6.0.646281499693 new feature

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

# train
print "start training...",len(x_train)
degree_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, ydegree_train)
print "degree feature:",degree_model.feature_importances_

# evaluate
print "start evaluating...",len(x_valid)
degree_ac=accuracy_score(ydegree_valid, degree_model.predict(x_valid))
print degree_ac

# predict
print "start build degree model..."
degree_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, ydegree)

print "start predicting..."
foutdegree=open("../out/result_degree_"+VERSION+".csv","w")
foutdegree.write("id,degree\n")
ydegree_test=degree_model.predict(x_test)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outdegree=[test_id[i],str(int(ydegree_test[i]))]
    foutdegree.write(",".join(outdegree)+"\n")
foutdegree.close()