# -*- coding:utf-8 -*-

from version import *
from common_chinese import *
from common_num import *
import json

def human_feat(jsonobj):
    retval=[jsonobj["id"],format_major(jsonobj["major"])]
    if jsonobj["gender"]=="女": retval.append(1)
    else: retval.append(0)
    return retval

def make_feat(inpath,outpath,isTrain=True):
    fin,fout=open(inpath),open(outpath,"w")
    title="id,major,gender,workage,average_salary,average_size,average_workmonth,last_position,next_position," \
          "before_workmonth,salary_gap,size_gap,total_workmonth,last_department,next_department,last_salary," \
          "last_size,last_workmonth,next_workmonth,next_salary,next_size,work_num,firstlast_sameindustry"
    if isTrain: title+=",ydegree,ysize,ysalary,yposition"
    fout.write(title+"\n")
    for line in fin:
        age,tsalary,tsize,tdur,bdur,bdept,ndept,jsonobj=0,0,0,0,0,0,0,json.loads(line)
        fposition,wn=0,len(jsonobj["workExperienceList"])

        # format every work experience
        fsalary,lsalary,bsalary,fsize,bsize,lsize,findustry,lindustry,bposition,nposition,bworkmonth,nworkmonth=0,0,0,0,0,0,None,None,0,0,0,0
        bpos_name,npos_name,sd_str,bd_str,ed_str="","",None,None,None
        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            # if test, skip column that to be predicted
            if w is None: continue
            # if train, but work experience less than 3
            if isTrain and wn<3: continue

            # about position_name
            position_name=w["position_name"].replace(" ","")
            if wn>2 and i==2: bposition=format_position(position_name)
            if i==0: nposition=format_position(position_name)

            # about salary
            tsalary+=int(w["salary"])*10
            if i==0: lsalary=int(w["salary"])
            if i==wn-1: fsalary=int(w["salary"])
            if i==2: bsalary=int(w["salary"])

            # about size
            tsize+=int(w["size"])*10
            if i==wn-1: fsize=int(w["size"])
            if i==0: lsize=int(w["size"])
            if i==2: bsize=int(w["size"])

            # about duration
            if w["start_date"] is None or w["end_date"] is None: continue
            else:
                sd=w["start_date"].replace(" ","")
                ed=w["end_date"].replace(" ","")
            duri=date_diff(sd,ed)
            if i==0: nworkmonth,ed_str=duri,ed
            if i==wn-1: sd_str=sd
            if wn>2 and i==2: bworkmonth,bd_str=duri,ed

            # about industry
            if i==wn-1: findustry=w["industry"]
            if i==0: lindustry=w["industry"]

            # about department
            if wn>2 and i==2: bdept=format_dept(w["department"])
            if i==0: ndept=format_dept(w["department"])

            # about label
            if isTrain and i==1:
                ysize=w["size"]
                ysalary=w["salary"]
                yposition=format_position(position_name)

        tdur=date_diff(sd_str,ed_str)
        bdur=date_diff(sd_str,bd_str)
        try:
            if jsonobj["age"][-1]=="岁": age=int(jsonobj["age"][:-1])
            else: age=int(jsonobj["age"])
        except:
            age=100
        if isTrain and (age-tdur>30 or age==100 or age-tdur/12<16): continue
        # start join feature
        outlist=human_feat(jsonobj)
        outlist+=[age-tdur/12,tsalary/wn,tsize/wn,tdur/wn,bposition,nposition,bdur,lsalary-fsalary,
                 lsize-fsize,tdur,bdept,ndept,bworkmonth,nworkmonth,bsalary,bsize,lsalary,lsize,wn]

        if findustry and lindustry and findustry==lindustry: outlist.append(1)
        else: outlist.append(0)

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