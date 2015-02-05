import elementtree.ElementTree as et
import re
import pickle
import tree
import sys
import os
from path import path

#argv[1]: morph.xml; argv[2]: ..._f/00/

def extractPosLex(node):
    global extMorph
    if node.tag == "Leafnode":
        pair = (node.attrib["pos"],node.attrib["lexeme"])
        if pair not in extMorph:
            extMorph.append(pair)
    else:
        for e in node:
            extractPosLex(e)
        

morphF = path(sys.argv[1])
bklDir = path(sys.argv[2])
#testF = path("ccgDeri_f/00/wsj_0001.xml")

#read in all pos-word pairs from morph file
morphTree = et.parse(morphF)
morphRoot = morphTree.getroot()

print morphRoot.tag

allMorph = []
for e in morphRoot:
    allMorph.append((e.attrib["pos"],e.attrib["word"]))

print len(allMorph)


#extract pos-word pairs from bkl parses
extMorph = []
for f in bklDir.files():
    print f
    Ftree = et.parse(f)
    FRoot = Ftree.getroot()
    for n in FRoot:
        extractPosLex(n)

print len(extMorph)

#add unseen morphs from extMorph to allMorph
unseen = []
for m in extMorph:
    if m not in allMorph:
        unseen.append(m)

print unseen, len(unseen)

#write new morph file
output = et.Element("morph")
for e in morphRoot:
    output.append(e)
for m in unseen:
    entry = et.Element("entry")
    entry.attrib["pos"] = m[0]
    entry.attrib["word"]= m[1]
    entry.tail = "\n"
    output.append(entry)
Etree = et.ElementTree(output)
Etree.write("morph.xml")
