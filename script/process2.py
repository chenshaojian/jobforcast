# -*- coding:utf-8 -*-

import json,sys
reload(sys)
sys.setdefaultencoding('utf-8')

def format_age(agestr):
    if agestr=="未知": return 0
    return agestr if agestr[-1:]!="岁" else agestr[:-1]

major_cnt,major_map=1,{}
def format_major(majorstr):
    global major_cnt
    if majorstr is None: return 0
    majorstr.replace(" ","")
    if majorstr not in major_map:
        major_map[majorstr]=major_cnt
        major_cnt+=1
    return major_map[majorstr]

dept_cnt,dept_map=1,{}
def format_dept(departstr):
    global dept_cnt
    if departstr is None: return 0
    departstr.replace(" ","")
    if departstr not in dept_map:
        dept_map[departstr]=dept_cnt
        dept_cnt+=1
    return dept_map[departstr]

position_map={u"技术支持":1, u"开发工程师":2,u"质量(QA/QC)":3,u"软件测试":4,u"机械工程师":5,u"会计":6,u"财务":7,u"项目经理":8,
              u"客服经理":9,u"客服":10,u"销售总监":11,u"销售经理":12,u"销售专员":13,u"市场总监":14,u"市场经理":15,u"市场专员":16,
              u"采购总监":17,u"采购经理":18,u"采购助理":19,u"生产总监":20,u"生产经理":21,u"生产专员":22,u"物流总监":23,u"物流经理":24,
              u"物流专员":25,u"运营总监":26,u"运营经理":27,u"运营专员":28,u"后勤主管":29,u"后勤专员":30,u"人力资源经理":31,u"人力资源专员":32}

def format_position(positionstr):
    if positionstr in position_map: return position_map[positionstr]
    return 0

def date_diff(sdate,edate):
    try:
        if edate=="Present" or edate=="至今" or edate=="今": edate="2015-09"
        syear,smonth=map(int,sdate.split("-"))
        eyear,emonth=map(int,edate.split("-"))
        return (eyear-syear)*12+(emonth-smonth)
    except:
        # print "except start_date or end_date:",sdate,edate
        return 0

def makefeat(inpath,outpath,isTrain=True):
    fin,fout=open(inpath),open(outpath,"w")
    for line in fin:
        tsalary,tsize,tdur,bdur,bdept,ndept,jsonobj=0,0,0,0,0,0,json.loads(line)
        fposition,wn=0,len(jsonobj["workExperienceList"])
        fmajor=format_major(jsonobj["major"])

        # format every work experience
        fsalary,lsalary,fsize,lsize,findustry,lindustry=0,0,0,0,None,None
        for i in xrange(wn):
            w=jsonobj["workExperienceList"][i]
            # if test, skip column that to be predicted
            if w is None: continue
            # if train, but no last second work experience
            if isTrain and wn<2: continue

            # about position_name
            position_name=w["position_name"].strip()
            if i==wn-1:
                aposition=format_position(position_name)
            if wn>2 and i==wn-3: bposition=format_position(position_name)
            else: bposition=0

            # about salary
            tsalary+=int(w["salary"])*10
            if i==0:
                fsalary=int(w["salary"])
            if i==wn-1:
                lsalary=int(w["salary"])

            # about size
            tsize+=int(w["size"])*10
            if i==0:
                fsize=int(w["size"])
            if i==wn-1:
                lsize=int(w["size"])

            # about duration
            if w["start_date"] is None or w["end_date"] is None: duri=0
            else: duri=date_diff(w["start_date"].strip(),w["end_date"].strip())
            tdur+=duri
            if i<wn-2:
                bdur+=duri

            # about industry
            if i==0: findustry=w["industry"]
            if i==wn-1: lindustry=w["industry"]

            # about department
            if wn>2 and i==wn-3: bdept=format_dept(w["department"])
            if i==wn-1: ndept=format_dept(w["department"])

            # about label
            if isTrain and i==wn-2:
                ysize=w["size"]
                ysalary=w["salary"]
                yposition=format_position(position_name)

        # 1.major
        # 2.average_salary
        # 3.average_size
        # 4.average_workmonth
        # 5.last_position
        # 6.next_position
        # 7.before_workmonth
        # 8.salary_gap
        # 9.size_gap
        # 10.total_workmonth
        # 11.last_department
        # 12.next_department
        outlist=[jsonobj["id"],fmajor,tsalary/wn,tsize/wn,tdur/wn,bposition,aposition,bdur,lsalary-fsalary,lsize-fsize,tdur,bdept,ndept]
        # 13.firstlast_sameindustry
        if findustry and lindustry and findustry==lindustry: outlist.append(1)
        else: outlist.append(0)
        # 14.gender
        if jsonobj["gender"]=="女": outlist.append(1)
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

print "make train feat..."
makefeat("../data/practice.json","../out/train2.txt")
print "make test feat..."
makefeat("../data/test.json","../out/test2.txt",False)