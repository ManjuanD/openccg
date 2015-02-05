import pickle
import re
from path import path
import elementtree.ElementTree as et
import sys

#unLabel takes a list of deps and takes off its label
def unLabel(l):
    unL = []
    for i in l:
        m = re.search("^.*(\(.*\))",i)
        if m != None:
            unD = m.group(1)
            unL.append(unD)
    return unL


#fscore takes two lists of deps and calcuate p,r and f1
def fscore(auto, gold):
    point = 0.0
#    scores = ()
    fs = 0.0
    pre = 0.0
    rec = 0.0
    for d in gold:
        if d in auto:
            point += 1
    if len(auto) != 0 and len(gold) != 0:
        pre = float(point)/len(auto)
        rec = float(point)/len(gold)
    if pre != 0 and rec != 0:
        fs = float(2*pre*rec)/(pre + rec)
    scores = (fs, pre, rec)
    return scores[1]

#take off the prefix "ID=" from the sentence id if any
def takeOffPrefix(dic):
    newDic = {}
    for s in dic:
        newId = re.sub("ID=","", s)
        newDic[newId] = dic[s]
    return newDic


goldDep = pickle.load(open(sys.argv[1],"rb"))
autoDep = pickle.load(open(sys.argv[2],"rb"))
#for d in goldDep:
#    print d, goldDep[d]
#    break


print "number of gold sentences:", len(goldDep)
print "number of auto sentences:", len(autoDep)

num = 0
OSum = 0
OSLsum = 0
for d in autoDep:
    if d in goldDep:
        num += 1
#        BS = fscore(unLabel(bklDep[d]),unLabel(goldDep[d]))
#        Bsum += BS
#        BklScoreNl[d] = BS
        OSL = fscore(autoDep[d],goldDep[d])
        OSLsum += OSL
        OS = fscore(unLabel(autoDep[d]),unLabel(goldDep[d]))
        OSum += OS
#        OpcScoreNl[d] = OS

print "Dependency accuracy is calculated on ", num, " auto-parses."
print "Labelled Accuracy:", float(OSLsum)/num,num
print "Unlabelled Accuracy:", float(OSum)/num,num
