# -*- coding:utf-8 -*-

from version import *
import json

def format_age(agestr):
    if agestr=="未知": return 0
    return agestr if agestr[-1:]!="岁" else agestr[:-1]

def format_major(majorstr):
    if majorstr is None: return 0
    majorstr.replace(" ","")
    if "计算机" in majorstr or "软件" in majorstr or "程序" in majorstr or "网络" in majorstr or "安全" in majorstr or "编程" in majorstr or "游戏" in majorstr: return 2
    if "MBA" in majorstr or "MPA" in majorstr or "精算" in majorstr or "证券" in majorstr or "销售" in majorstr or "财经" in majorstr or "银行" in majorstr or "商业" in majorstr or "营销" in majorstr or "贸易" in majorstr or "财务" in majorstr or "经营" in majorstr or "财会" in majorstr or "商务" in majorstr or "金融" in majorstr or "税务" in majorstr or "货运" in majorstr or "管理" in majorstr or "经济" in majorstr or "市场" in majorstr or "财政" in majorstr or "保险" in majorstr or "会计" in majorstr or "投资" in majorstr or "审计" in majorstr or "保险" in majorstr or "房地产" in majorstr or "资产" in majorstr: return 3
    if "电子" in majorstr or "微波" in majorstr or "电气" in majorstr or "控制" in majorstr or "无线电" in majorstr or "通讯" in majorstr or "通信" in majorstr or "测控" in majorstr or "自动化" in majorstr or "信息" in majorstr or "数控" in majorstr or "计量" in majorstr or "检测技术" in majorstr or "仪器" in majorstr: return 4
    if "土木" in majorstr or "排水" in majorstr or "建筑" in majorstr or "道路" in majorstr or "规划" in majorstr or "测绘" in majorstr or "交通" in majorstr: return 5
    if "数学" in majorstr or "数理" in majorstr or "统计" in majorstr or "物理" in majorstr: return 6
    if "生物" in majorstr or "生命" in majorstr or "生化" in majorstr or "材料" in majorstr or "加工工艺" in majorstr or "环境" in majorstr or "钳工" in majorstr or "激光" in majorstr or "焊接" in majorstr or "液压" in majorstr or "铸造" in majorstr or "焊接" in majorstr or "冶金" in majorstr or "金属" in majorstr: return 7
    if "力学" in majorstr or "机械" in majorstr or "机电" in majorstr or "能源" in majorstr or "热能" in majorstr or "锻造" in majorstr or "轧钢" in majorstr or "制造" in majorstr or "工业" in majorstr or "工程" in majorstr: return 8
    if "法学" in majorstr or "民法" in majorstr or "政法" in majorstr or "法律" in majorstr or "司法" in majorstr or "政治" in majorstr or "律师" in majorstr or "行政" in majorstr or "公共" in majorstr or "社会" in majorstr or "人力" in majorstr: return 9
    if "化学" in majorstr or "化工" in majorstr: return 10
    if "心理" in majorstr: return 11
    if "语言" in majorstr or "翻译" in majorstr or "口译" in majorstr or "广播" in majorstr or "韩语" in majorstr or "汉语" in majorstr or "韩国语" in majorstr or "日本语" in majorstr or "中文" in majorstr or "西班牙语" in majorstr or "朝鲜语" in majorstr or "外语" in majorstr or "文学" in majorstr or "德语" in majorstr or "英语" in majorstr or "日语" in majorstr or "俄语" in majorstr or "法语" in majorstr or "播音" in majorstr or "新闻" in majorstr or "传播" in majorstr or "广告" in majorstr or "阿拉伯语" in majorstr: return 12
    if "艺术" in majorstr or "雕塑" in majorstr or "电影" in majorstr or "舞蹈" in majorstr or "电视" in majorstr or "传媒" in majorstr or "声乐" in majorstr or "传达" in majorstr or "媒体" in majorstr or "设计" in majorstr or "绘画" in majorstr or "影视" in majorstr or "导演" in majorstr or "表演" in majorstr or "动画" in majorstr or "音乐" in majorstr or "摄影" in majorstr or "美术" in majorstr: return 13
    if "医学" in majorstr or "病理" in majorstr or "外科" in majorstr or "临床" in majorstr or "妇产" in majorstr or "医疗" in majorstr or "推拿" in majorstr or "眼科" in majorstr or "内科" in majorstr or "药物" in majorstr or "中药" in majorstr or "药学" in majorstr or "药理" in majorstr or "中医" in majorstr or "西医" in majorstr or "药剂" in majorstr or "制药" in majorstr or "护理" in majorstr: return 14
    if "教育" in majorstr: return 15
    if "园林" in majorstr or "畜牧" in majorstr or "养殖" in majorstr or "森林" in majorstr or "农村" in majorstr or "农学" in majorstr or "园艺" in majorstr or "农业" in majorstr or "环艺" in majorstr: return 16
    if "食品" in majorstr or "烹饪" in majorstr or "餐饮" in majorstr or "厨师" in majorstr: return 17
    if "出版" in majorstr or "印刷" in majorstr: return 18
    if "汽车" in majorstr or "电工" in majorstr or "汽修" in majorstr or "维修" in majorstr or "汽配" in majorstr: return 19
    if "航空" in majorstr: return 20
    if "服装" in majorstr or "纺织" in majorstr or "染整" in majorstr: return 21
    if "历史" in majorstr: return 22
    if "运动" in majorstr or "体育" in majorstr: return 23
    if "文秘" in majorstr or "秘书" in majorstr: return 24
    if "地质" in majorstr or "地理" in majorstr or "矿山" in majorstr or "大气" in majorstr or "水处理" in majorstr: return 25
    if "电力" in majorstr or "供电" in majorstr or "配电" in majorstr: return 26
    if "动物" in majorstr or "兽医" in majorstr or "植物" in majorstr or "林学" in majorstr: return 27
    if "哲学" in majorstr or "伦理学" in majorstr: return 28
    if "海洋" in majorstr or "航海" in majorstr: return 29
    if "旅游" in majorstr: return 30
    if "服役" in majorstr or "兵役" in majorstr: return 31
    if "珠宝" in majorstr or "宝石" in majorstr: return 32
    if "物流" in majorstr or "运输" in majorstr: return 33
    if "装潢" in majorstr or "建材" in majorstr: return 34
    if "刑事" in majorstr or "侦查" in majorstr or "治安" in majorstr or "公安" in majorstr or "监狱" in majorstr or "罪犯" in majorstr: return 35
    if "档案" in majorstr or "图书馆" in majorstr: return 36
    if "制冷" in majorstr or "空调" in majorstr or "暖通" in majorstr: return 37
    if "导游" in majorstr: return 38
    if "外交" in majorstr or "国际关系" in majorstr: return 39
    if "党史" in majorstr or "文史" in majorstr: return 40
    if "空乘" in majorstr: return 41
    if "师范" in majorstr or "幼师" in majorstr: return 42
    if "内审" in majorstr: return 43
    if "物业" in majorstr: return 44
    if "驾驶" in majorstr or "司机" in majorstr: return 45
    if "酿造" in majorstr: return 46
    if "人类学" in majorstr: return 47
    if "生态学" in majorstr: return 48
    if "油气" in majorstr: return 49
    if "茶学" in majorstr: return 50
    if "草业" in majorstr: return 51
    if "培训" in majorstr or "教育" in majorstr: return 52
    if "指挥" in majorstr or "武器" in majorstr: return 53
    if "商品学" in majorstr: return 54
    if "情报学" in majorstr: return 55
    if "生理学" in majorstr: return 56
    if "模具" in majorstr: return 57
    if "电脑" in majorstr: return 94
    if "经理" in majorstr: return 95
    if "工民建" in majorstr: return 96
    if "文科" in majorstr or "理科" in majorstr or "本科" in majorstr or "理工" in majorstr or "普高" in majorstr or "大专" in majorstr or "高中" in majorstr or "学生" in majorstr: return 97
    if "无" in majorstr or "其他" in majorstr or "其它" in majorstr: return 98
    if majorstr[-3:]=="中": return 99
    return 1

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

def upper_lower_relation(lname,rname):
    if rname[-2:]==u"经理" and lname[-2:]==u"专员": return 1
    if rname[-2:]==u"总监" and lname[-2:]==u"经理": return 1
    else: return 2

def format_position(positionstr):
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

def makefeat(inpath,outpath,isTrain=True):
    fin,fout=open(inpath),open(outpath,"w")
    title="id,workage,major,average_salary,average_size,average_workmonth,last_position,next_position," \
          "before_workmonth,salary_gap,size_gap,total_workmonth,last_department,next_department," \
          "firstlast_sameindustry,gender,last_workmonth,next_workmonth"
    if isTrain: title+=",ydegree,ysize,ysalary,yposition"
    fout.write(title+"\n")
    for line in fin:
        age,tsalary,tsize,tdur,bdur,bdept,ndept,jsonobj=0,0,0,0,0,0,0,json.loads(line)
        fposition,wn=0,len(jsonobj["workExperienceList"])
        fmajor=format_major(jsonobj["major"])

        # format every work experience
        fsalary,lsalary,fsize,lsize,findustry,lindustry,bposition,nposition,bworkmonth,nworkmonth=0,0,0,0,None,None,0,0,0,0
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

            # about size
            tsize+=int(w["size"])*10
            if i==wn-1: fsize=int(w["size"])
            if i==0: lsize=int(w["size"])

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
        if age-tdur>30 or age==100 or age-tdur/12<16: continue
        # 1.workage
        # 2.major
        # 3.average_salary
        # 4.average_size
        # 5.average_workmonth
        # 6.last_position
        # 7.next_position
        # 8.before_workmonth
        # 9.salary_gap
        # 10.size_gap
        # 11.total_workmonth
        # 12.last_department
        # 13.next_department
        outlist=[jsonobj["id"],age-tdur/12,fmajor,tsalary/wn,tsize/wn,tdur/wn,bposition,nposition,bdur,lsalary-fsalary,lsize-fsize,tdur,bdept,ndept]
        # 14.firstlast_sameindustry
        if findustry and lindustry and findustry==lindustry: outlist.append(1)
        else: outlist.append(0)
        # 15.gender
        if jsonobj["gender"]=="女": outlist.append(1)
        else: outlist.append(0)
        # 16.last_workmonth
        outlist.append(bworkmonth)
        # 17.next_workmonth
        outlist.append(nworkmonth)

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
makefeat("../data/train.json","../out/train"+VERSION+".csv")
print "make test feat..."
makefeat("../data/test.json","../out/test"+VERSION+".csv",False)