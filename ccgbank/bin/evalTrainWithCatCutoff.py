import path
import elementtree.ElementTree as et
import re
import pickle
import sys
import os

#read categories from an element recursively
#return a dic with cat as the key and freq as value
def read_cat(elem):
    global catDic
    global posDic
    if "stag" in elem.attrib:
        if elem.attrib["stag"] not in catDic:
            catDic[(elem.attrib["stag"])]=1
        else:
            catDic[(elem.attrib["stag"])]+=1
    if elem.tag == "Leafnode":
        if elem.attrib["pos"] not in posDic:
            posDic[(elem.attrib["pos"])]=1
        else:
            posDic[(elem.attrib["pos"])]+=1
    for elem2 in elem:
        read_cat(elem2)
#    return catDic

#read categories from an element, returning a list
def read_cat_list(elem):
    global catList
    if "stag" in elem.attrib:
        if elem.attrib["stag"] not in catList:
            catList.append(elem.attrib["stag"])
        
    for elem2 in elem:
        read_cat_list(elem2)
    return catList


catDic = {}
posDic = {}
for p, subdirs, files in os.walk(r'convert/'):
    print p
    if p != "convert/":
        ccgDir = path.path(p)
        for f in ccgDir.files():
            ccgTree = et.parse(f)
            ccgRoot = ccgTree.getroot()
            for e in ccgRoot:
                read_cat(e)

print "There are totally", len(catDic), "categories in OpenCCG."
print "There are totally", len(posDic), "POS tags in OpenCCG."

#give each category a pseudo name for training
lowFreqCat = []
catList = []
catMatch = {}
catMatchLow = {}
n = 0
for c in catDic:
    n += 1
    newLabel = "C"+str(n)+"SC"
    catMatch[c] = newLabel
    if catDic[c]>10 or catDic[c]==10:
        catMatchLow[c] = newLabel
    else:
        lowFreqCat.append(c)


pickle.dump(catMatchLow, open("catMatchWithCutoff.pkl", "wb"))
pickle.dump(catMatch, open("catMatch.pkl", "wb"))
pickle.dump(lowFreqCat, open("lowFreqCats.pkl", "wb"))
print "There are", len(lowFreqCat), "low-freq (< 10)categories."
print "After deleting low-freq categories, we have", len(catMatchLow), "categories."

#catMatchLow = pickle.load(open("catMatchWithCutoff.pkl","rb"))
#
#punctMatch = {}
#punctMatch[","]="punct[,]"
#punctMatch[":"]="punct[:]"
#punctMatch[";"]="punct[;]"
#punctMatch["rrb"]="punct[-rRB-]"
#
missHeader = 0
fileList = []
lowFreqFiles = []
excludes = ["convert/","convert/00", "convert/01", "convert/23", "convert/24"]
totalSen = []

# cfgDev: Sect 00; cfgTrain: Sect 02-21

for p, subdirs, files in os.walk(r'convert/'):

    if p not in excludes:
        ccgDir = path.path(p)
        for f in ccgDir.files():
            ccg_tree = et.parse(f)
            ccg_root = ccg_tree.getroot()
            
            for e in ccg_root:
                if "Header" in e.attrib:
                    filename = e.attrib["Header"]
                    if filename not in totalSen:
                        totalSen.append(filename)
                    catList = []
                    read_cat_list(e)
                    if len(set(catList).intersection(set(lowFreqCat)))== 0:
                        #print "delete this sentence from training", filename
                        if filename not in fileList:
                            fileList.append(filename)
                    else:
                        if filename not in lowFreqFiles:
                            lowFreqFiles.append(filename)
                else:
                    #print "missing head"
                    missHeader += 1
                    


print "Total number of sentences in original training set:", len(totalSen)
print "Sentences having low-freq cats:", len(lowFreqFiles)
print "Size of new training corpus:", len(fileList)

