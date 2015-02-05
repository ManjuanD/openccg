import sys
import pickle

string = {}
n = 0
for line in file(sys.argv[1]):
    n += 1
    key = "S"+str(n)
    string[key] = line.strip()

pickle.dump(string, open("stringIndex.pkl","wb"))
print "totally", len(string), "sentences are in novel text."

