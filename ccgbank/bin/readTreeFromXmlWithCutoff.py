import path
import elementtree.ElementTree as et
import re
import pickle
import sys
import os
import tree

def tree_from_lf(elem, match):
    global line
    if elem.tag == "Leafnode":
        lex = elem.attrib["lexeme"]
        pos = elem.attrib["pos"]
        #replace ccg cats with fake cats
        cat = match[elem.attrib["stag"]]
        line = line + "("+cat +" (" + pos + " " + lex  + ") " + ")"
#        print line
    elif elem.tag == "Treenode":
        if "stag" in elem.attrib:
            if elem.attrib["stag"] in punctMatch:
                punctCat = punctMatch[elem.attrib["stag"]]
                cat = catMatch[punctCat]
                print elem.attrib["stag"], punctCat
            else:
                cat = match[elem.attrib["stag"]]                
            line = line + "(" + cat + " "
        else:
            for a in elem.attrib:
                print a, elem.attrib[a]
        for elem2 in elem:
            tree_from_lf(elem2, match)
        line = line + ")"
#        print line
    else:
        for elem3 in elem:
            tree_from_lf(elem3, match)
    return line


#read categories from an element, returning a list                                                                                         
def read_cat_list(elem):
    global catList
    if "stag" in elem.attrib:
        if elem.attrib["stag"] not in catList:
            catList.append(elem.attrib["stag"])

    for elem2 in elem:
        read_cat_list(elem2)
    return catList

    
catMatchLow = pickle.load(open("catMatchWithCutoff.pkl","rb"))
catMatch = pickle.load(open("catMatch.pkl","rb"))
lowFreqCat = pickle.load(open("lowFreqCats.pkl", "rb"))
print "total number of cats:", len(catMatch)
print "total number of low-freq cats:", len(lowFreqCat)
print "total number of freq-cat:", len(catMatchLow)

#catCount = pickle.load(open("catCount.pkl","rb"))
#lowFreqCat = []
#for c in catCount:
#    if catCount[c]<10:
#        lowFreqCat.append(c)
#print "number of low-freq cats", len(lowFreqCat)

#fileList = pickle.load(open("fileList.pkl","rb"))
#print "number of sentences ", len(fileList)

#t = 0
#for c in catMatch:
#    t += 1
#    if t < 10:
#        print c, catMatch[c]

#change the following four catgories in training
punctMatch = {}
punctMatch[","]="punct[,]"
punctMatch[":"]="punct[:]"
punctMatch[";"]="punct[;]"
punctMatch["rrb"]="punct[-rRB-]"

#inputPath = "convert/" + sys.argv[1] + "/"

missHeader = 0
notTrain = ["convert/", "convert/00", "convert/01", "convert/23", "convert/24"]
dev = ["convert/00"]
test23=["convert/23"]
test24=["convert/24"]

# cfgDev: Sect 00; cfgTrain: Sect 02-21
#cfgDir = path.path("cfgDev/")
#lowFreqNum = 0

#os.mkdir("cfgWithCutoff/")
#cfgDir = path.path("cfgWithCutoff/")

#if not os.path.exists("devTrees"):
#    os.makedirs("devTrees")
#
#if not os.path.exists("trainTrees"):
#    os.makedirs("trainTrees")
#
#devDir = path.path("devTrees/")
#trainDri = path.path("trainTrees/")

devTrees = open("dev.linetrees", "wb")
trainTrees = open("train.linetrees", "wb")
test23Trees = open("test23.linetrees", "wb")
test24Trees = open("test24.linetrees", "wb")
dev_string = {}
train_string = {}
test23_string = {}
test24_string = {}
ms= 0

for p, subdirs, files in os.walk(r'convert/'):
    print p
    if p in dev:
        print p, "goes into dev"
        ccgDir = path.path(p)
        for f in ccgDir.files():
#            print "filename", f
            ccg_tree = et.parse(f)
            ccg_root = ccg_tree.getroot()
            for e in ccg_root:
                if "Header" in e.attrib:
                    header = e.attrib["Header"]
#                    print "senID", header
                    line = "( "
                    lineTree = tree_from_lf(e, catMatch)
                    lineTree = lineTree + ")\n"
                    devTrees.write(lineTree)
                    t = tree.Tree()
                    t.read(lineTree.strip())
                    string = re.sub(" +", " ", t.leaf())
                    dev_string[header] = string
#                    print string
                else:
                    ms += 1
                    header = "Missing"+str(ms)
#                    print header
                    line = "( "
                    lineTree = tree_from_lf(e, catMatch)
                    lineTree = lineTree + ")\n"
                    devTrees.write(lineTree)
                    t = tree.Tree()
                    t.read(lineTree.strip())
                    string = re.sub(" +", " ", t.leaf())
                    dev_string[header] = string
                
    elif p in test23:
        print p, "goes into test23"
        ccgDir = path.path(p)
        for f in ccgDir.files():
            ccg_tree = et.parse(f)
            ccg_root = ccg_tree.getroot()
            for e in ccg_root:
                if "Header" in e.attrib:
                    header = e.attrib["Header"]
#                    print "senID", header
                    line = "( "
                    lineTree = tree_from_lf(e, catMatch)
                    lineTree = lineTree + ")\n"
                    test23Trees.write(lineTree)
                    t = tree.Tree()
                    t.read(lineTree.strip())
                    string = re.sub(" +", " ", t.leaf())
                    test23_string[header] = string
#                    print string
                else:
                    ms += 1
                    header = "Missing"+str(ms)
#                    print header
                    line = "( "
                    lineTree = tree_from_lf(e, catMatch)
                    lineTree = lineTree + ")\n"
                    test23Trees.write(lineTree)
                    t = tree.Tree()
                    t.read(lineTree.strip())
                    string = re.sub(" +", " ", t.leaf())
                    test23_string[header] = string
    elif p in test24:
        print p, "goes into test24"
        ccgDir = path.path(p)
        for f in ccgDir.files():
            ccg_tree = et.parse(f)
            ccg_root = ccg_tree.getroot()
            for e in ccg_root:
                if "Header" in e.attrib:
                    header = e.attrib["Header"]
#                    print "senID", header
                    line = "( "
                    lineTree = tree_from_lf(e, catMatch)
                    lineTree = lineTree + ")\n"
                    test24Trees.write(lineTree)
                    t = tree.Tree()
                    t.read(lineTree.strip())
                    string = re.sub(" +", " ", t.leaf())
                    test24_string[header] = string
#                    print string
                else:
                    ms += 1
                    header = "Missing"+str(ms)
#                    print header
                    line = "( "
                    lineTree = tree_from_lf(e, catMatch)
                    lineTree = lineTree + ")\n"
                    test24Trees.write(lineTree)
                    t = tree.Tree()
                    t.read(lineTree.strip())
                    string = re.sub(" +", " ", t.leaf())
                    test24_string[header] = string
    elif p not in notTrain:
        print p, "goes into training"
        ccgDir = path.path(p)
        for f in ccgDir.files():
            ccg_tree = et.parse(f)
            ccg_root = ccg_tree.getroot()
            for e in ccg_root:                
                if "Header" in e.attrib:
                    header = e.attrib["Header"]
                    catList = []
                    read_cat_list(e)
                    if len(set(catList).intersection(set(lowFreqCat)))== 0:
                        line = "( "
                        lineTree = tree_from_lf(e, catMatchLow)
                        lineTree = lineTree + ")\n"
                        trainTrees.write(lineTree)
                        t = tree.Tree()
                        t.read(lineTree.strip())
                        string = re.sub(" +", " ", t.leaf())
                        train_string[header] = string
                else:
                    ms += 1
                    header = "Missing"+str(ms)
#                    print header
                    catList = []
                    read_cat_list(e)
                    if len(set(catList).intersection(set(lowFreqCat)))== 0:
                        line = "( "
                        lineTree = tree_from_lf(e, catMatchLow)
                        lineTree = lineTree + ")\n"
                        trainTrees.write(lineTree)
                        t = tree.Tree()
                        t.read(lineTree.strip())
                        string = re.sub(" +", " ", t.leaf())
                        train_string[header] = string
                        
devTrees.close()
trainTrees.close()
test23Trees.close()
test24Trees.close()

pickle.dump(dev_string, open("dev.string", "wb"))
pickle.dump(train_string, open("train.string", "wb"))
pickle.dump(test23_string, open("test23.string", "wb"))
pickle.dump(test24_string, open("test24.string", "wb"))

print len(dev_string)
print len(train_string)
print len(test23_string)
print len(test24_string)
