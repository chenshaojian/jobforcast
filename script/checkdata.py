# -*- coding:utf-8 -*-

from version import *

def check(path,fnum):
    suc,fin=0,open(path)
    fin.readline()
    for line in fin:
        fields=line.split(",")
        if len(fields)!=fnum:
            print line[:-1]
            continue
        suc+=1
    fin.close()
    print path,suc

print "check train..."
check("../out/train"+VERSION+".csv",28)
print "check test..."
check("../out/test"+VERSION+".csv",24)