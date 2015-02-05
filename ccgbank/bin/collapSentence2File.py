from path import path
import elementtree.ElementTree as et
import re
import pickle
import tree
import sys
import os

def getFn(f):
    global inP
    fn = ''
    fn = re.sub(inP,"",f)
    fn = re.sub("/ID=","",fn)
    fn = re.sub("\..*", "",fn)
    return fn

def getSenId(f):
    global inP
    fn = ''
    fn = re.sub(inP,"",f)
    fn = re.sub("\.xml", "",fn)
    return fn

inP = sys.argv[1]
inputDir = path(inP)
outputDir = sys.argv[2]

#establish a list for every file
fileLs = []
for f in inputDir.files():
    fn = getFn(f)
#    print fn
    if fn not in fileLs:
        fileLs.append(fn)
#print len(fileLs)
for f in fileLs:
    fname = f + ".xml"
    root = et.Element("Derivation")
    root.text = "\n"
    for s in inputDir.files():
        if getFn(s) == f:
            sentence = et.parse(s)
            s_root = sentence.getroot()
            for tnode in s_root:
                root.append(tnode)
    Etree = et.ElementTree(root)
    Etree.write(outputDir+fname)
                
            
