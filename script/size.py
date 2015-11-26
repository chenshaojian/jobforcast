# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

# 1.0.519155910674
# 2.0.39233763573 remove posset,indusset,descendsize
# 3.0.40340094243 add first,last,next industry
# 4.0.40544970293 add first-last,first-next indus,size,salary,pos,poslevel,firstposlevel

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

# train
print "start training...",len(x_train)
size_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, ysize_train)
print "size feature:",size_model.feature_importances_

# evaluate
print "start evaluating...",len(x_valid)
size_ac=accuracy_score(ysize_valid, size_model.predict(x_valid))
print size_ac

# predict
print "start build size model..."
size_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, ysize)

print "start predicting..."
foutsize=open("../out/result_size_"+VERSION+".csv","w")
foutsize.write("id,size\n")
ysize_test=size_model.predict(x_test)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outsize=[test_id[i],str(int(ysize_test[i]))]
    foutsize.write(",".join(outsize)+"\n")
foutsize.close()