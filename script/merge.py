from version import *

fdegree=open("../out/result_degree_"+VERSION+".csv")
fsize=open("../out/result_size_"+VERSION+".csv")
fsalary=open("../out/result_salary_"+VERSION+".csv")
fposition=open("../out/result_position_"+VERSION+".csv")

fout=open("../out/result"+VERSION+".csv","w")
fout.write("id,degree,size,salary,position_name\n")

degreelines=fdegree.readlines()
sizelines=fsize.readlines()
salarylines=fsalary.readlines()
positionlines=fposition.readlines()

for i in xrange(1,len(degreelines)):
    f1=degreelines[i].split(",")
    f2=sizelines[i].split(",")
    f3=salarylines[i].split(",")
    f4=positionlines[i].split(",")
    fout.write(f1[0]+","+f1[1][:-1]+","+f2[1][:-1]+","+f3[1][:-1]+","+f4[1])
fout.close()
fdegree.close()
fsize.close()
fsalary.close()
fposition.close()