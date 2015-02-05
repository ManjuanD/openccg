from path import path
import elementtree.ElementTree as et
import re
import pickle
import sys

def getPosName(e):
    pos = e.attrib["pos"]
    if ":" in e.attrib["name"]:
        m = re.match("(^.*):.*$",e.attrib["name"])
        name = m.group(1)
    else:
        name = e.attrib["name"]
    return (pos,name)


ipLex = sys.argv[1]
ipTree = et.parse(ipLex)
ipRoot = ipTree.getroot()
op_dir = path(sys.argv[2])

opRoot = et.Element("ccg-lexicon")

for attr in ipRoot.attrib:
    opRoot.attrib[attr] =  ipRoot.attrib[attr]
    opRoot.text = "\n"

memD = {}
for i in ipRoot:
    if i.tag == "family":
        sp = getPosName(i)
        if sp not in memD:
            memD[sp] = []
            if i.attrib["closed"] == "true":
                for m in i:
                    if m.tag == "member":
                        memD[sp].append(m)
        else:
            if i.attrib["closed"] == "true":
                for m in i:
                    if m.tag == "member":
                        if m not in memD[sp]:
                            memD[sp].append(m)



spList = []
#using the first family defined for certain (pos name) pair as its structure 
for node in ipRoot:
    if node.tag != "family":
        opRoot.append(node)
    else:
        sp = getPosName(node)
        if sp not in spList:
            spList.append(sp)
            opRoot.append(node)
            # if it is closed family, copy all the members over
            if node.attrib["closed"]== "true":
                for m in memD[sp]:
                    node.append(m)


#collapse pred/sense to the most frequently used ones for each stem
for i in opRoot:
   if i.tag == "family":
        if i.attrib["closed"] == "true":
                stemList = []
                predDict = {}

                for elem in i.findall("member"):
                    stem = elem.attrib["stem"]
                    #we want to keep all the senses of "be" and "have"
                    if stem == "have" or elem.attrib["stem"] == "be":
                        continue

                    if stem not in predDict:
                        predDict[stem] = []

                    if stem not in stemList:
                        stemList.append(stem)
                    else:
                        if "pred" in elem.attrib:
                            match = re.search("^.*\.(.*)$", elem.attrib["pred"])
                            if match != None:
                                if match.group(1).isdigit():
                                    num = int(match.group(1))
                                else:
                                    num = 100
                                predDict[stem].append(num)
                        i.remove(elem)
                for stem in sorted(predDict):
                    if len(predDict[stem])!= 0:
                        member = et.Element("member")
                        member.attrib["stem"] = stem
                        leastNum = min(predDict[stem])
                        if leastNum == 100:
                            member.attrib["pred"] = stem + ".XX"
                        else:
                            member.attrib["pred"] = stem + ".0"+str(leastNum)
                        member.tail = "\n"
                        i.append(member)



Etree = et.ElementTree(opRoot)
Etree.write(op_dir/"simplified-lexicon.xml")
#et.dump(opRoot)
