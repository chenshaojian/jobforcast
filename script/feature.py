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
    common_title= "id,major,gender,age,workage,worknum,beforeworktime,indusnum,posnum,poslevelnum,lastworktime,nextworktime"
    degree_title=common_title+",firstsize,firstsalary,avesize,avesalary,aveworktime,maxposlevel"
    size_title=common_title+",firstsize,lastsize,nextsize,lastposition,nextposition,descendsize"
    salary_title=common_title+",firstsalary,lastsalary,nextsalary,lastposition,nextposition,descendsalary"
    position_title=common_title+",maxposlevel,lastsize,nextsize,lastsalary,nextsalary,lastposlevel,nextposition,lastposlevel,nextposlevel,descendposlevel"
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

        # format every work experience
        bworktime,tworktime,lastworktime,nextworktime=0,0,0,0
        indusset,posset,poslevelset=set(),set(),set()
        tsize,tsalary=0,0
        maxposlevel,lastposlevel,nextposlevel=0,0,0
        descendsize,descendsalary,descendposlevel=0,0,0

        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            # if test, skip column that to be predicted
            if w is None: continue

            # position name
            poslevel,position_name=format_position(w["position_name"])
            posset.add(position_name)
            poslevelset.add(poslevel)
            maxposlevel=max(maxposlevel,poslevel)
            if i==0:
                nextposition=position_name
                nextposlevel=position_name
            if i==2:
                lastposition=position_name
                lastposlevel=position_name
            if i>1 and jsonobj["workExperienceList"][i-1]:
                pposlevel,_=format_position(jsonobj["workExperienceList"][i-1]["position_name"])
                if poslevel<pposlevel: descendposlevel=1

            # industry
            industry_name=format_industry(w["industry"])
            indusset.add(industry_name)

            # size
            if i==0: nextsize=int(w["size"])
            if i==2: lastsize=int(w["size"])
            if i==wn-1: firstsize=int(w["size"])
            if i>1:
                tsize+=int(w["size"])
                if jsonobj["workExperienceList"][i-1] and int(w["size"])<int(jsonobj["workExperienceList"][i-1]["size"]):
                    descendsize=1

            # salary
            if i==0: nextsalary=int(w["salary"])
            if i==2: lastsalary=int(w["salary"])
            if i==wn-1: firstsalary=int(w["salary"])
            if i>1:
                tsalary+=int(w["salary"])
                if jsonobj["workExperienceList"][i-1] and int(w["salary"])<int(jsonobj["workExperienceList"][i-1]["salary"]):
                    descendsalary=1

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
        salary_title=common_title+",firstsalary,lastsalary,nextsalary,lastposition,nextposition,descendsalary"
        position_title=common_title+",maxposlevel,lastposlevel,nextposition,lastposlevel,nextposlevel,descendposlevel"

        commonlist=[age-tworktime/12,wn,bworktime,len(indusset),len(posset),len(poslevelset),lastworktime,nextworktime]
        degreelist=outlist+commonlist+[firstsize,firstsalary,round(float(tsize)/(wn-2)),
                                       round(float(tsalary)/(wn-2)),round(float(bworktime)/(wn-2)),maxposlevel]
        sizelist=outlist+commonlist+[firstsize,lastsize,nextsize,lastposition,nextposition,descendsize]
        salarylist=outlist+commonlist+[firstsalary,lastsalary,nextsalary,lastposition,nextposition,descendsalary]
        positionlist=outlist+commonlist+[maxposlevel,lastsize,nextsize,lastsalary,nextsalary,lastposition,
                                         nextposition,lastposlevel,nextposlevel,descendposlevel]

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