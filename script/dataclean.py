# -*- coding:utf-8 -*-

from version import *
from common_num import *
import json
import codecs

def isValidTime(t):
    if t is None or t=="" or t=="1970-01": return False
    return True

def filterSample(inpath,outpath):
    fin,fout,okcnt=codecs.open(inpath,"r"),codecs.open(outpath,"w","utf-8"),0
    for line in fin:
        okPos,okSD,okED,jsonobj,untilnow=True,True,True,json.loads(line,"utf-8"),0
        wn=len(jsonobj["workExperienceList"])

        for i in xrange(wn):
            work=jsonobj["workExperienceList"][i]
            pwork=jsonobj["workExperienceList"][i+1] if i<wn-1 else None
            nwork=jsonobj["workExperienceList"][i-1] if i>0 else None

            # fix invalid work time
            if not isValidTime(work["start_date"]) and pwork is not None and isValidTime(pwork["end_date"]):
                work["start_date"]=pwork["end_date"]
            elif not isValidTime(work["start_date"]):
                continue
            if not isValidTime(work["end_date"]) and nwork is not None and isValidTime(nwork["start_date"]):
                work["end_date"]=nwork["start_date"]
            elif not isValidTime(work["end_date"]):
                continue

            sd,ed=work["start_date"].replace(" ",""),work["end_date"].replace(" ","")
            if u"今" in ed or "Present" in ed:
                if i==wn-1: work["end_date"]="2015-09"
                elif nwork is not None: work["end_date"]=nwork["start_date"]
                else: untilnow+=1

            # filter by position_name
            if i==1 and work["position_name"] not in position_map: okPos=False

        if okPos and untilnow<=1:
            fout.write(json.dumps(jsonobj,ensure_ascii=False)+"\n")
            # fout.write(line)
            okcnt+=1
    fin.close()
    fout.close()
    print okcnt

if __name__=="__main__":
    print "filter train data..."
    filterSample("../data/practice.json","../data/train"+VERSION+".json")