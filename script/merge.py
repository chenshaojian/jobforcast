f1,f2=open("result.csv"),open("result2.csv")
lines1,lines2=f1.readlines(),f2.readlines()
f1.close()
f2.close()
fo=open("out.csv","w")
fo.write(lines1[0])
for i in xrange(1,len(lines1)):
    fields1=lines1[i].split(",")
    fields2=lines2[i].split(",")
    fields2[-1]=fields1[-1]
    fo.write(",".join(fields2))
fo.close()