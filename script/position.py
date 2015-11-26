# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

# 1.0.638598647818
# 2.0.565662774022 remove posset,indusset,descendposlevel
# 3.0.576213890596 add first,last,next industry
# 4.0.578774841221 add first-last,first-next indus,size,salary,pos,poslevel,firstposlevel
# 5.0.575804138496 merge to one feature list
# 6.0.568018848597

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

# train
print "start training...",len(x_train)
position_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, yposition_train)
print "position feature:",position_model.feature_importances_

# evaluate
print "start evaluating...",len(x_valid)
position_ac=accuracy_score(yposition_valid, position_model.predict(x_valid))
print position_ac

# predict
print "start build position model..."
position_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, yposition)

print "start predicting..."
foutposition=open("../out/result_position_"+VERSION+".csv","w")
foutposition.write("id,position\n")
yposition_test=position_model.predict(x_test)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outposition=[test_id[i],position_map2[int(yposition_test[i])]]
    foutposition.write(",".join(outposition)+"\n")
foutposition.close()