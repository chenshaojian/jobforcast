# -*- coding:utf-8 -*-

from version import *
from common_chinese import *
from common_num import *
import json

def human_feat(jsonobj):
    retval=[jsonobj["id"],format_major(jsonobj["major"])]
    if jsonobj["gender"]=="女": retval.append(1)
    else: retval.append(0)
    try:
        if jsonobj["age"][-1]=="岁": age=int(jsonobj["age"][:-1])
        else: age=int(jsonobj["age"])
    except:
        age=100
    retval.append(age)
    return age,retval

def make_feat(inpath,outpath,isTrain=True):
    fin,fout=open(inpath),open(outpath,"w")
    title="id,major,gender,age,workage,worknum,beforeworktime,posnum,indusnum," \
          "firstsize,firstsalary,lastworktime,lastsize,lastsalary,lastindus,lastposition," \
          "nextworktime,nextsize,nextsalary,nextindus,nextposition"
    if isTrain: title+=",ydegree,ysize,ysalary,yposition"
    fout.write(title+"\n")

    for line in fin:
        jsonobj=json.loads(line)
        wn=len(jsonobj["workExperienceList"])
        # if train, but work experience less than 3
        if isTrain and wn<3: continue

        # format every work experience
        bworktime,tworktime,lastworktime,nextworktime,posset,indusset,tsize,tsalary=0,0,0,0,set(),set(),0,0
        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            # if test, skip column that to be predicted
            if w is None: continue

            # position name
            _,position_name=format_position(w["position_name"])
            posset.add(position_name)
            if i==0: nextposition=position_name
            if i==2: lastposition=position_name

            # industry
            industry_name=format_industry(w["industry"])
            indusset.add(industry_name)
            if i==0: nextindustry=industry_name
            if i==2: lastindustry=industry_name

            # size
            if i==0: nextsize=int(w["size"])
            if i==2: lastsize=int(w["size"])
            if i==wn-1: firstsize=int(w["size"])
            if i>1: tsize+=int(w["size"])

            # salary
            if i==0: nextsalary=int(w["salary"])
            if i==2: lastsalary=int(w["salary"])
            if i==wn-1: firstsalary=int(w["salary"])
            if i>1: tsalary+=int(w["salary"])

            # worktime
            # about duration
            if w["start_date"] is None or w["end_date"] is None: continue
            else:
                sd=w["start_date"].replace(" ","")
                ed=w["end_date"].replace(" ","")
            duration=date_diff(sd,ed)
            if i==0: nextworktime=duration
            if i>1: bworktime+=duration
            if i==2: lastworktime=duration
            tworktime+=duration

            # about label
            if isTrain and i==1:
                ysize=w["size"]
                ysalary=w["salary"]
                _,yposition=format_position(w["position_name"])

        # start join feature
        age,outlist=human_feat(jsonobj)

        # skip after feature generation
        if isTrain and (age==100 or age-tworktime/12>30 or age-tworktime/12<16): continue

        # make other feature
        outlist+=[age-tworktime/12,wn,bworktime,len(posset),len(indusset),
                  firstsize,firstsalary,lastworktime,lastsize,lastsalary,lastindustry,lastposition,
                  nextworktime,nextsize,nextsalary,nextindustry,nextposition]

        # if train, print label column
        if isTrain:
            outlist.append(jsonobj["degree"])
            outlist.append(ysize)
            outlist.append(ysalary)
            outlist.append(yposition)

        # skip position_name label not in [1-32]
        if isTrain and yposition==0: continue
        fout.write(",".join(map(str,outlist))+"\n")

    fin.close()
    fout.close()

if __name__=="__main__":
    print "make train feat..."
    make_feat("../data/train"+VERSION+".json","../out/train"+VERSION+".csv")
    print "make test feat..."
    make_feat("../data/test.json","../out/test"+VERSION+".csv",False)