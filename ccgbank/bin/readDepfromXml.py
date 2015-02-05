from path import path
import elementtree.ElementTree as et
import re
import pickle
import sys
import os

#get_fullword takes a full-word.text and returns a list of full-words
def get_fullwords(fullWord):
    surList = {}
    testStr = re.sub(re.escape("\n"), re.escape("\\n"),fullWord)
    wordList = re.split(' ', testStr)
    for i in range(1, len(wordList)-1):
        m = re.match('(^.*):S-.*',wordList[i])
        if m != None:
            sur = re.sub("&apos;", "'", m.group(1))
            sur = re.sub("&#45;", "-", sur)
            sur = re.sub("&amp;", "&", sur)
            sur = re.sub("\\/", "/", sur)
            surList[i-1] = sur
        else:
            print "check fullword", senId
    return surList

def get_dep_from_lf(n, surList):
    global depList
    if n.tag =="node":
        h_idx = 0
        if len(n.findall("rel"))!= 0:
            if "id" in n.attrib:
                head_idx = n.attrib["id"]
                m = re.match('w([0-9]+).*',head_idx)
                if m != None:
                    h_idx = int(m.group(1))
            elif "idref" in n.attrib:
                head_idx = n.attrib["idref"]
                m = re.match('w([0-9]+).*',head_idx)
                if m != None:
                    h_idx = int(m.group(1))                
#            print "idx", idx
            head = surList[h_idx]
#            print "head", head
            for r in n:
                if r.tag == "rel":
                    rel = r.attrib["name"]
#                print "rel", rel
                    for n1 in r:
                        c_idx = 0
                        if "id" in n1.attrib:
                            child_idx = n1.attrib["id"]
                            m = re.match('w([0-9]+).*',child_idx)
                            if m != None:
                                c_idx = int(m.group(1))
                        elif "idref" in n1.attrib:
                            child_idx = n1.attrib["idref"]
                            m = re.match('w([0-9]+).*',child_idx)
                            if m!= None:
                                c_idx = int(m.group(1))
#                    print "idx child", idx
                        child = surList[c_idx]
#                    print "child", child
                        dep = rel + "(" + head + ", "+ child + ")"
#                print dep
                        depList.append(dep)
    for e in n:
        get_dep_from_lf(e, surList)
    return depList

inputDir = path(sys.argv[1])
#outputDir = path(sys.argv[2])
#if not os.path.exists(sys.argv[2]):
#    os.makedirs(sys.argv[2])


outDep = {}
for f in inputDir.files():
    if f.ext == ".xml":
        lf = et.parse(f)
        lfRoot = lf.getroot()

        for item in lfRoot:

            fn = item.attrib["info"]
#            print fn
            surList = {}
            depList = []
            for e in item:
                if e.tag == "full-words":
                    surList = get_fullwords(e.text)

            for e in item:
                if e.tag == "lf":
                    for n in e:
                        get_dep_from_lf(n,surList)
    
#            output = open(outputDir/fn, "wb")
#            for dep in depList:
#                output.write(dep+"\n")
#            output.close()
            outDep[fn] = depList
            depList = []

print "Total number of sentences:", len(outDep)
#for i in outDep:
#    print i, outDep[i]
#    break

pickle.dump(outDep, open(sys.argv[2],"wb"))
