# -*- coding:utf-8 -*-

from version import *
from common_chinese import *
from common_num import *
import json

# id, major, gender, age
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

def make_feat(inpath,outdegree,outsize,outsalary,outposition,isTrain=True):
    fin,fdgree,fsize,fsalary,fposition=open(inpath),open(outdegree,"w"),open(outsize,"w"),open(outsalary,"w"),open(outposition,"w")

    # feature title
    common_title="id,major,gender,age,workage,worknum,beforeworktime,firstindus," \
                 "flindus,fnindus,firstposlevel"
    ws_common_title=",lastworktime,nextworktime,lastdus,nextdus,poslevelnum," \
                    "maxsize_salary,maxsize_poslevel,maxsize_position,maxsize_worktime," \
                    "maxsalary_size,maxsalary_poslevel,maxsalary_position,maxsalary_worktime," \
                    "maxposlevel_size,maxposlevel_salary,maxposlevel_position,maxposlevel_worktime," \
                    "maxworktime_size,maxworktime_salary,maxworktime_poslevel,maxworktime_position"
    degree_title=common_title+ws_common_title+",firstsize,firstsalary,avesize,avesalary,aveworktime,firstposition"
    size_title=common_title+ws_common_title+",firstsize,lastsize,nextsize,flsize,fnsize,desclnsize"
    salary_title=common_title+ws_common_title+",firstsalary,lastsalary,nextsalary,flsalary,fnsalary,desclnsalary"
    position_title=common_title+ws_common_title+",lastposition,nextposition,lastposlevel,nextposlevel," \
                                                "flpos,fnpos,flposlevel,fnposlevel,desclnposlevel"
    if isTrain:
        degree_title+=",ydegree"
        size_title+=",ysize"
        salary_title+=",ysalary"
        position_title+=",yposition"

    fdgree.write(degree_title+"\n")
    fsize.write(size_title+"\n")
    fsalary.write(salary_title+"\n")
    fposition.write(position_title+"\n")

    # make feature sample by sample
    for line in fin:
        jsonobj=json.loads(line)
        wn=len(jsonobj["workExperienceList"])
        # if train, but work experience less than 3
        if isTrain and wn<3: continue

        # every feature variable definition
        bworktime,tworktime,lastworktime,nextworktime=0,0,0,0   # time
        poslevelset=set()   # poslevel set
        tsize,tsalary=0,0   # total size, salary
        firstposition,lastposition,nextposition=0,0,0   # position
        firstposlevel,lastposlevel,nextposlevel=0,0,0   # poslevel
        firstindus,lastdus,nextdus=0,0,0    # industry
        flindus,fnindus,flsize,fnsize,flsalary,fnsalary,flpos,fnpos,flposlevel,fnposlevel=0,0,0,0,0,0,0,0,0,0   # diff
        desclnsize,desclnsalary,desclnposlevel=0,0,0    # descend
        maxsize,maxsize_salary,maxsize_poslevel,maxsize_position,maxsize_worktime=0,0,0,0,0
        maxsalary,maxsalary_size,maxsalary_poslevel,maxsalary_position,maxsalary_worktime=0,0,0,0,0
        maxposlevel,maxposlevel_size,maxposlevel_salary,maxposlevel_position,maxposlevel_worktime=0,0,0,0,0
        maxworktime,maxworktime_size,maxworktime_salary,maxworktime_poslevel,maxworktime_position=0,0,0,0,0

        # iterate every work experience
        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            # if test, skip column that to be predicted
            if w is None: continue

            # position name
            poslevel,position_name=format_position(w["position_name"])
            poslevelset.add(poslevel)
            if i==0:
                nextposition=position_name
                nextposlevel=poslevel
            if i==2:
                lastposition=position_name
                lastposlevel=poslevel
                if nextposlevel<lastposlevel: desclnposlevel=1
            if i==wn-1:
                firstposition=position_name
                if firstposition==lastposition: flpos=1
                if firstposition==nextposition: fnpos=1
                firstposlevel=poslevel
                if firstposlevel==lastposlevel: flposlevel=1
                if firstposlevel==nextposlevel: fnposlevel=1

            # industry
            industry_name=format_industry(w["industry"])
            if i==wn-1:
                firstindus=industry_name
                if firstindus==lastdus: flindus=1
                if firstindus==nextdus: fnindus=1
            if i==2: lastdus=industry_name
            if i==0: nextdus=industry_name

            # size
            size=int(w["size"])
            if i==0: nextsize=size
            if i==2:
                lastsize=size
                if nextsize<lastsize: desclnsize=1
            if i==wn-1:
                firstsize=size
                if firstsize==lastsize: flsize=1
                if firstsize==nextsize: fnsize=1
            if i>1:
                tsize+=int(w["size"])

            # salary
            salary=int(w["salary"])
            if i==0: nextsalary=salary
            if i==2:
                lastsalary=salary
                if nextsalary<lastsalary: desclnsalary=1
            if i==wn-1:
                firstsalary=salary
                if firstsalary==lastsalary: flsalary=1
                if firstsalary==nextsalary: fnsalary=1
            if i>1:
                tsalary+=salary

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

            # joint feature
            if i!=1 and poslevel>=maxposlevel:
                maxposlevel=poslevel
                maxposlevel_size=size
                maxposlevel_salary=salary
                maxposlevel_position=position_name
                maxposlevel_worktime=duration
            if i!=1 and size>=maxsize:
                maxsize=size
                maxsize_salary=salary
                maxsize_poslevel=poslevel
                maxsize_position=position_name
                maxsize_worktime=duration
            if i!=1 and salary>=maxsalary:
                maxsalary=salary
                maxsalary_size=size
                maxsalary_poslevel=poslevel
                maxsalary_position=position_name
                maxsalary_worktime=duration
            if i!=1 and poslevel>=maxposlevel:
                maxposlevel=poslevel
                maxposlevel_size=size
                maxposlevel_salary=salary
                maxposlevel_position=position_name
                maxposlevel_worktime=duration
            if i!=1 and duration>=maxworktime:
                maxworktime=duration
                maxworktime_size=size
                maxworktime_salary=salary
                maxworktime_poslevel=poslevel
                maxworktime_position=position_name

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
        commonlist=[age-tworktime/12,wn,bworktime,firstindus,flindus,fnindus,firstposlevel]
        ws_commonlist=[lastworktime,nextworktime,lastdus,nextdus,len(poslevelset),
                       maxsize_salary,maxsize_poslevel,maxsize_position,maxsize_worktime,
                       maxsalary_size,maxsalary_poslevel,maxsalary_position,maxsalary_worktime,
                       maxposlevel_size,maxposlevel_salary,maxposlevel_position,maxposlevel_worktime,
                       maxworktime_size,maxworktime_salary,maxworktime_poslevel,maxworktime_position]
        degreelist=outlist+commonlist+ws_commonlist+[firstsize,firstsalary,round(float(tsize)/(wn-2)),
                                                     round(float(tsalary)/(wn-2)),round(float(bworktime)/(wn-2)),firstposition]
        sizelist=outlist+commonlist+ws_commonlist+[firstsize,lastsize,nextsize,flsize,fnsize,desclnsize]
        salarylist=outlist+commonlist+ws_commonlist+[firstsalary,lastsalary,nextsalary,flsalary,fnsalary,desclnsalary]
        positionlist=outlist+commonlist+ws_commonlist+[lastposition,nextposition,lastposlevel,nextposlevel,flpos,fnpos,
                                         flposlevel,fnposlevel,desclnposlevel]

        # if train, print label column
        if isTrain:
            degreelist+=[jsonobj["degree"]]
            sizelist+=[ysize]
            salarylist+=[ysalary]
            positionlist+=[yposition]

        # skip position_name label not in [1-32]
        if isTrain and yposition==0: continue

        fdgree.write(",".join(map(str,degreelist))+"\n")
        fsize.write(",".join(map(str,sizelist))+"\n")
        fsalary.write(",".join(map(str,salarylist))+"\n")
        fposition.write(",".join(map(str,positionlist))+"\n")

    fin.close()
    fdgree.close()
    fsize.close()
    fsalary.close()
    fposition.close()

if __name__=="__main__":
    print "make train feat..."
    make_feat("../data/train"+VERSION+".json","../out/train_degree_"+VERSION+".csv","../out/train_size_"+VERSION+".csv",
              "../out/train_salary_"+VERSION+".csv","../out/train_position_"+VERSION+".csv")
    print "make test feat..."
    make_feat("../data/test.json","../out/test_degree_"+VERSION+".csv","../out/test_size_"+VERSION+".csv",
              "../out/test_salary_"+VERSION+".csv","../out/test_position_"+VERSION+".csv",False)