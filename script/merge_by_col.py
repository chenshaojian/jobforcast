from version import *

def merge(f1path,f2path,col1,col2,outpath):
    f1=open(f1path)
    f2=open(f2path)
    fout=open(outpath,"w")

    f1lines=f1.readlines()
    f2lines=f2.readlines()

    fout.write(f1lines[0])

    for i in xrange(1,len(f1lines)):
        f1fields=f1lines[i][:-1].split(",")
        f2fields=f2lines[i][:-1].split(",")
        outlist=[]
        for c in col1:
            outlist.append(f1fields[c])
        for c in col2:
            outlist.insert(c,f2fields[c])
        fout.write(",".join(outlist)+"\n")

    f1.close()
    f2.close()
    fout.close()

merge("../out/result.csv","../out/result13.csv",[0,1,2,4],[3],"../out/result000.csv")