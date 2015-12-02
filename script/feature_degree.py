# -*- coding:utf-8 -*-

from version import *
from common_num import *
import json

def make_feat(inpath,outpath,isTrain=True):
    fin,fout=open(inpath),open(outpath,"w")

    fout.write("id,major,gender,first_work_age,first_industry,first_size,first_salary,first_poslevel,"
               "total_worktime_per_work,total_worktime_per_industry,average_salary,firstmaxposworktime")
    if isTrain:
        fout.write(",ydegree\n")
    else:
        fout.write("\n")

    # make feature sample by sample
    for line in fin:
        jsonobj=json.loads(line)
        wn=len(jsonobj["workExperienceList"])
        # if train, but work experience less than 3
        if isTrain and wn<3: continue

        tworktime,tsalary,maxposlevel=0,0,0
        industryset=set()

        # iterate every work experience
        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            # if test, skip column that to be predicted
            if w is None: continue

            # position name
            poslevel,position_name=format_position(w["position_name"])
            if i==wn-1: first_poslevel=poslevel

            # industry
            industry_name=format_industry(w["industry"])
            industryset.add(industry_name)
            if i==wn-1: first_industry=industry_name

            # size
            size=int(w["size"])
            if i==wn-1: first_size=size

            # salary
            salary=int(w["salary"])
            if i==wn-1: first_salary=salary
            tsalary+=10*salary

            # worktime
            if w["start_date"] is None or w["end_date"] is None: continue
            else:
                sd=w["start_date"].replace(" ","")
                ed=w["end_date"].replace(" ","")
            worktime=date_diff(sd,ed)
            tworktime+=worktime

            if poslevel>=maxposlevel:
                firstmaxposworktime=tworktime
                maxposlevel=poslevel

            # label
            if isTrain and i==1:
                _,yposition=format_position(w["position_name"])

        # start join feature
        age,outlist=human_feat(jsonobj)

        # skip after feature generation
        if isTrain and (age==100 or age-tworktime/12>30 or age-tworktime/12<16): continue

        # id,major,gender,first_work_age,first_industry,first_size,first_salary,first_poslevel,
        # total_worktime_per_work,total_worktime_per_industry,average_salary,firstmaxposworktime
        featlist=outlist[:3]+[age-tworktime/12,first_industry,first_size,first_salary,first_poslevel,tworktime/wn,
                              tworktime/len(industryset),tsalary/wn,(tworktime-firstmaxposworktime)/12]

        # if train, print label column
        if isTrain:
            featlist+=[jsonobj["degree"]]

        # skip position_name label not in [1-32]
        if isTrain and yposition==0: continue

        fout.write(",".join(map(str,featlist))+"\n")

    fin.close()
    fout.close()

if __name__=="__main__":
    print "make train feat..."
    make_feat("../data/train"+VERSION+".json","../out/train_degree_"+VERSION+".csv")
    print "make test feat..."
    make_feat("../data/test.json","../out/test_degree_"+VERSION+".csv",False)
    # for p in otherposition:
    #     print p