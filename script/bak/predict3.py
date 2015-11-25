# -*- coding:utf-8 -*-

from version import *

position_map={1:u"技术支持", 2:u"开发工程师",3:u"质量(QA/QC)",4:u"软件测试",5:u"机械工程师",6:u"会计",7:u"财务",8:u"项目经理",
              9:u"客服经理",10:u"客服",11:u"销售总监",12:u"销售经理",13:u"销售专员",14:u"市场总监",15:u"市场经理",16:u"市场专员",
              17:u"采购总监",18:u"采购经理",19:u"采购助理",20:u"生产总监",21:u"生产经理",22:u"生产专员",23:u"物流总监",24:u"物流经理",
              25:u"物流专员",26:u"运营总监",27:u"运营经理",28:u"运营专员",29:u"后勤主管",30:u"后勤专员",31:u"人力资源经理",32:u"人力资源专员"}

from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split

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
yposition_train, yposition_valid = train_test_split(x, ydegree, ysize, ysalary, yposition, test_size=0.33, random_state=82)

# handle test data
fin2.readline()
for line in fin2:
    fields=line.split(",")
    test_id.append(fields[0])
    # remove test id
    x_test.append(map(float,fields[1:]))
fin2.close()

# train
print "start training...",len(x_train)
degree_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x_train, ydegree_train)
print "degree feature:",degree_model.feature_importances_

size_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x_train, ysize_train)
print "size feature:",size_model.feature_importances_

salary_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x_train, ysalary_train)
print "salary feature:",salary_model.feature_importances_

position_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x_train, yposition_train)
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

# predict
print "start build degree model..."
degree_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x, ydegree)
print "start build size model..."
size_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x, ysize)
print "start build salary model..."
salary_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x, ysalary)
print "start build position model..."
position_model = GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=3, random_state=0).fit(x, yposition)

print "start predicting..."
fout=open("../out/result"+VERSION+".csv","w")
fout.write("id,degree,size,salary,position_name\n")
ydegree_test=degree_model.predict(x_test)
ysize_test=size_model.predict(x_test)
ysalary_test=salary_model.predict(x_test)
yposition_test=position_model.predict(x_test)

# output result
print "start output..."
for i in xrange(len(test_id)):
    outlist=[test_id[i],str(int(ydegree_test[i])),str(int(ysize_test[i])),str(int(ysalary_test[i])),position_map[int(yposition_test[i])]]
    fout.write(",".join(outlist)+"\n")
fout.close()