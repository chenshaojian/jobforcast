# -*- coding:utf-8 -*-

from version import *
from common_num import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
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

min_max_scaler = preprocessing.MinMaxScaler()
x = np.array(x)
x = min_max_scaler.fit_transform(x)

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

x_test = min_max_scaler.fit_transform(x_test)

# train
print "start training...",len(x_train)
degree_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, ydegree_train)
print "degree feature:",degree_model.feature_importances_

size_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, ysize_train)
print "size feature:",size_model.feature_importances_

salary_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, ysalary_train)
print "salary feature:",salary_model.feature_importances_

position_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x_train, yposition_train)
print "position feature:",position_model.feature_importances_

# evaluate
print "start evaluating...",len(x_valid)
degree_ac=accuracy_score(ydegree_valid, degree_model.predict(x_valid))
size_ac=accuracy_score(ysize_valid, size_model.predict(x_valid))
salary_ac=accuracy_score(ysalary_valid, salary_model.predict(x_valid))
position_ac=accuracy_score(yposition_valid, position_model.predict(x_valid))
print degree_ac,size_ac,salary_ac,position_ac

# 1. 0.606561524838 0.471114109809 0.710550729527 0.418402631357, online score: 0.33
# 2. 0.63277679321 0.551441096913 0.765506948979 0.408170879582
# 3. 0.637620192308 0.555488782051 0.792167467949 0.504907852564, online score: 0.4095
# 4. 0.655716294957 0.556560176813 0.777777777778 0.495077355837, online score: 0.4154
# 5. 0.663050030139 0.613220815752 0.802089612216 0.496885674101
# 6. 0.657790425856 0.701087508893 0.837788393129 0.501473727005
# 7. 0.661957516008 0.864823660941 0.925094013619 0.486329911576, online score: 0.35126057
# 8. 0.656994818653 0.414196891192 0.596373056995 0.530466321244, online score: 0.50951
# 9. 0.66103626943 0.393886010363 0.582694300518 0.554196891192
#10. 0.664413030117 0.39069862733 0.576623642696 0.560950624872
#11. 0.664105716042 0.520077852899 0.725978283139 0.643925425118, online score: 0.4373
#12. 0.660930137267 0.530219217373 0.733558696988 0.634091374718, online score: 0.4373

# predict
print "start build degree model..."
degree_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, ydegree)
print "start build size model..."
size_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, ysize)
print "start build salary model..."
salary_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, ysalary)
print "start build position model..."
position_model = GradientBoostingClassifier(n_estimators=TREENUM,learning_rate=LRATE,max_depth=TREEDEPTH, random_state=RANDSEED).fit(x, yposition)

print "start predicting..."
fout=open("../out/result"+VERSION+".csv","w")
fout.write("id,degree,size,salary,position_name\n")
ydegree_test=degree_model.predict(x_test)
ysize_test=size_model.predict(x_test)
ysalary_test=salary_model.predict(x_test)
yposition_test=position_model.predict(x_test)

# output result
print "start output...",len(test_id)
for i in xrange(len(test_id)):
    outlist=[test_id[i],str(int(ydegree_test[i])),str(int(ysize_test[i])),str(int(ysalary_test[i])),position_map2[int(yposition_test[i])]]
    fout.write(",".join(outlist)+"\n")
fout.close()