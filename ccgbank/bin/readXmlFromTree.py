from path import path
import elementtree.ElementTree as et
import re
import pickle
import tree
import sys
import editdist
import os

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def xml_from_tree(t, root, inv_match):
    if len(t.ch)==1 and len(t.ch[0].ch)==1 and t.ch[0].ch[0].ch==[]:
        e = et.Element("Leafnode")
#        cat = re.sub("\)", "", re.sub("\(","",t.c))
        e.attrib["stag"] = inv_match[t.c]
        e.attrib["cat"] = inv_match[t.c]
        e.attrib["pos"] = t.ch[0].c
        e.attrib["lexeme"] = t.ch[0].ch[0].c
#        e.tail = "\n"
        root.append(e)
    
    elif len(t.ch)!= 0 and t.ch[0].ch!= []:        
        e = et.Element("Treenode")
        cat = re.sub("\)", "", re.sub("\(","",t.c))
        e.attrib["stag"] = inv_match[t.c]
        e.attrib["cat"] = inv_match[t.c]
#        e.text = "\n"
#        e.tail = "\n"
        root.append(e)
        for c in t.ch:
            xml_from_tree(c, e, inv_match)

def find_filename(string, match):
    editD = 1000
    fn = ''
    for f in match:
        dis = editdist.distance(string, match[f])
        if dis < editD:
            editD = dis
            fn = f
    return fn

#input file is the output of parser
inputF = sys.argv[1]
if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])
outputDir = path(sys.argv[2])

#match:ccg-cat --> pesudo cat
#sys.argv[3] = ccgCatMatch.pkl or catMatchCutoff.pkl
match = pickle.load(open(sys.argv[3],"rb"))
#t = 0
#for m in match:
#    t += 1
#    if t < 10:
#        print m, match[m]

#the following two are for matching dev SENTENCE 
#fileName = pickle.load(open("fileStrMatch_dev.pkl", "rb"))
#fileName = pickle.load(open("gold_ccgstr.pkl", "rb"))

#this pkl file is for matching REALIZATION
#fileName = pickle.load(open("pctRealStr.pkl","rb"))
#sys.argv[4] is a dic of reference strings
ref_string= pickle.load(open(sys.argv[4],"rb"))
t  = 0 
for f in ref_string:
    t += 1
    if t < 10:
        print f, ref_string[f]

#make a dictionary with string as key and fn as value
str2fn = {}
for fn in ref_string:
    str2fn[ref_string[fn]] = fn

#inv_match: pseudo cat --> ccg cat
inv_match = {}
for c in match:
    inv_match[match[c]] = c

numParse = {}
lineNum = 0
n = 0
mis = 0
for line in file(inputF):
    if line[0] == "(" and len(line)>4:
        #take off the outmost brackets if it is not the output of grammarTester
        #line = line[2:-1]
        lineNum += 1
        t = tree.Tree()
        line = line.strip()
        t.read(line)
        string = re.sub(" +", " ",t.leaf())
        fn = find_filename(string, ref_string)
        print fn
        root = et.Element("Derivation")
        xml_from_tree(t,root, inv_match)
        indent(root)
        #add header infomation to the top treenode
        for d in root:
            if d.tag == "Treenode":
                d.attrib["Header"] = fn

        Etree = et.ElementTree(root)
        Etree.write(outputDir/fn)

#        if string not in numParse:
#            numParse[string] = 0
#        if string in str2fn:
#            numParse[string] += 1
#            fn = str2fn[string]
#            print fn
#            fname = fn+".p"+str(numParse[string])+".xml"
#            sId = fn+".p"+str(numParse[string])
#            root = et.Element("Derivation")
#            xml_from_tree(t,root, inv_match)
#            indent(root)
            #add header infomation to the top treenode
#            for d in root:
#                if d.tag == "Treenode":
#                    d.attrib["Header"] = fn

#            Etree = et.ElementTree(root)
#            Etree.write(outputDir/fn)
#        else:
#            mis +=1
#            print "cannot find this string", string



        
print "read out",lineNum, "derivations."
print "mis", mis
