# -*- coding:utf-8 -*-

def format_age(agestr):
    if agestr=="未知": return 0
    return agestr if agestr[-1:]!="岁" else agestr[:-1]

dept_cnt,dept_map=1,{}
def format_dept(departstr):
    global dept_cnt
    if departstr is None: return 0
    departstr.replace(" ","")
    if departstr not in dept_map:
        dept_map[departstr]=dept_cnt
        dept_cnt+=1
    return dept_map[departstr]

indus_cnt,indus_map=1,{}
def format_industry(industrystr):
    global indus_cnt
    if industrystr is None: return 0
    industrystr.replace(" ","")
    if industrystr not in indus_map:
        indus_map[industrystr]=indus_cnt
        indus_cnt+=1
    return indus_map[industrystr]

position_map={u"技术支持":1, u"开发工程师":2,u"质量(QA/QC)":3,u"软件测试":4,u"机械工程师":5,u"会计":6,u"财务":7,u"项目经理":8,
              u"客服经理":9,u"客服":10,u"销售总监":11,u"销售经理":12,u"销售专员":13,u"市场总监":14,u"市场经理":15,u"市场专员":16,
              u"采购总监":17,u"采购经理":18,u"采购助理":19,u"生产总监":20,u"生产经理":21,u"生产专员":22,u"物流总监":23,u"物流经理":24,
              u"物流专员":25,u"运营总监":26,u"运营经理":27,u"运营专员":28,u"后勤主管":29,u"后勤专员":30,u"人力资源经理":31,u"人力资源专员":32}

position_map2={1:u"技术支持", 2:u"开发工程师",3:u"质量(QA/QC)",4:u"软件测试",5:u"机械工程师",6:u"会计",7:u"财务",8:u"项目经理",
              9:u"客服经理",10:u"客服",11:u"销售总监",12:u"销售经理",13:u"销售专员",14:u"市场总监",15:u"市场经理",16:u"市场专员",
              17:u"采购总监",18:u"采购经理",19:u"采购助理",20:u"生产总监",21:u"生产经理",22:u"生产专员",23:u"物流总监",24:u"物流经理",
              25:u"物流专员",26:u"运营总监",27:u"运营经理",28:u"运营专员",29:u"后勤主管",30:u"后勤专员",31:u"人力资源经理",32:u"人力资源专员"}

def upper_lower_relation(lname,rname):
    if rname[-2:]==u"经理" and lname[-2:]==u"专员": return 1
    if rname[-2:]==u"总监" and lname[-2:]==u"经理": return 1
    else: return 2

def format_position(positionstr):
    if positionstr is None: return 0
    positionstr=positionstr.replace(" ","")
    if positionstr in position_map: return position_map[positionstr]
    return 0

def date_diff(sdate,edate):
    try:
        if sdate=="1970-01": return 0
        if edate=="Present" or edate=="至今" or edate=="今": edate="2015-09"
        syear,smonth=map(int,sdate.split("-"))
        eyear,emonth=map(int,edate.split("-"))
        return (eyear-syear)*12+(emonth-smonth)
    except:
        # print "except start_date or end_date:",sdate,edate
        return 0