# -*- coding:utf-8 -*-

from version import *
from common_num import *
import json
import numpy as np

def make_feat(inpath,outpath,isTrain=True):
    fin,fout=open(inpath),open(outpath,"w")

    fout.write("id,major,gender,before_worktime,ln_worktime,last_poslevel,last_size,ln_size,most_size,"
               "ln_poslevel,next_poslevel,next_size,last_worktime,next_worktime,"
               "size_in_industry_level")
    if isTrain:
        fout.write(",ysize\n")
    else:
        fout.write("\n")

    samples=fin.readlines()
    fin.close()

    industry_size={}

    # get 3 kinds of size percentile
    for sample in samples:
        jsonobj=json.loads(sample)
        wn=len(jsonobj["workExperienceList"])
        # if train, but work experience less than 3
        if isTrain and wn<3: continue

        tworktime,maxsize=0,0

        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            if w is None: continue

            _,position_name=format_position(w["position_name"])
            industry_name=format_industry(w["industry"])
            size=int(w["size"])
            if size>maxsize: maxsize=size

            if industry_name not in industry_size: industry_size[industry_name]=[size]
            else: industry_size[industry_name].append(size)

            if w["start_date"] is None or w["end_date"] is None: continue
            else:
                sd=w["start_date"].replace(" ","")
                ed=w["end_date"].replace(" ","")
            worktime=date_diff(sd,ed)
            tworktime+=worktime

        age,outlist=human_feat(jsonobj)
        if isTrain and (age==100 or age-tworktime/12>30 or age-tworktime/12<16): continue

    for k,v in industry_size.iteritems():
        val,a=[],np.array(v)
        for i in xrange(20,100,20):
            val.append(np.percentile(a,i))
        industry_size[k]=val

    # make feature sample by sample
    for sample in samples:
        jsonobj=json.loads(sample)
        wn=len(jsonobj["workExperienceList"])
        # if train, but work experience less than 3
        if isTrain and wn<3: continue

        bworktime,tworktime,lworktime,nworktime,maxposlevel,maxsize,maxsize_industry=0,0,0,0,0,0,0
        sizefreq={}
        mostsize,mostsize_tmp=0,0

        # iterate every work experience
        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            # if test, skip column that to be predicted
            if w is None: continue

            # position name
            poslevel,position=format_position(w["position_name"])
            if i==2:
                last_position=position_name
                last_poslevel=poslevel
            if i==0:
                next_position=position_name
                next_poslevel=poslevel

            # industry
            industry_name=format_industry(w["industry"])

            # size
            size=int(w["size"])
            if i==2: last_size=size
            if i==0: next_size=size
            if size>maxsize:
                maxsize=size
                maxsize_industry=industry_name
            if size in sizefreq: sizefreq[size]+=1
            else: sizefreq[size]=1
            if sizefreq[size]>mostsize_tmp:
                mostsize_tmp=sizefreq[size]
                mostsize=size

            # salary
            salary=int(w["salary"])
            if i==2: last_salary=salary
            if i==0: next_salary=salary

            # worktime
            if w["start_date"] is None or w["end_date"] is None: continue
            else:
                sd=w["start_date"].replace(" ","")
                ed=w["end_date"].replace(" ","")
            worktime=date_diff(sd,ed)
            tworktime+=worktime
            if i>1: bworktime+=worktime
            if i==2:
                tmp_start=ed
                lworktime=worktime
            if i==0:
                tmp_end=sd
                nworktime=worktime
            if i==wn-1: ln_worktime=date_diff(tmp_start,tmp_end)

            if poslevel>=maxposlevel:
                firstmaxposworktime=tworktime
                maxposlevel=poslevel

            # label
            if isTrain and i==1:
                _,yposition=format_position(w["position_name"])
                ysize=w["size"]

        # start join feature
        age,outlist=human_feat(jsonobj)

        # skip after feature generation
        if isTrain and (age==100 or age-tworktime/12>30 or age-tworktime/12<16): continue

        industry_sizelevel=0
        for percent in industry_size[maxsize_industry]:
            if maxsize>=percent: industry_sizelevel+=1

        # id,major,gender,before_worktime,ln_worktime,last_poslevel,last_size,ln_size,most_size
        # ln_poslevel,next_poslevel,next_size,last_worktime,next_worktime
        # size_in_industry_level
        featlist=outlist[:3]+[bworktime,ln_worktime,last_poslevel,last_size,next_size-last_size,mostsize,
                              next_poslevel-last_poslevel,next_poslevel,next_size,lworktime,nworktime,
                              industry_sizelevel]

        # if train, print label column
        if isTrain:
            featlist+=[ysize]

        # skip position_name label not in [1-32]
        if isTrain and yposition==0: continue

        fout.write(",".join(map(str,featlist))+"\n")

    fout.close()

if __name__=="__main__":
    print "make train feat..."
    make_feat("../data/train"+VERSION+".json","../out/train_size_"+VERSION+".csv")
    print "make test feat..."
    make_feat("../data/test.json","../out/test_size_"+VERSION+".csv",False)