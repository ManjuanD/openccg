import re
#import sys

# a Tree consists of a category label 'c' and a list of child Trees 'ch'
class Tree:
    
    # obtain tree from string
    def read(this,s):
        this.ch = []
        # a tree can be just a terminal symbol (a leaf)
        m = re.search('^ *([^ ()]+) *(.*)',s)
        if m != None:
            this.c = m.group(1)
            return m.group(2)
        # a tree can be an open paren, nonterminal symbol, subtrees, close paren
#        m = re.search('^ *\( *([^ ()]*) *(.*)',s)
        m = re.search('^ *\( *([^ ]*) *(.*)',s)
        if m != None:
            this.c = m.group(1)
            s = m.group(2)
            while re.search('^ *\)',s) == None:
                t = Tree()
                s = t.read(s)
                this.ch = this.ch + [t]
            return re.search('^ *\) *(.*)',s).group(1)
        return ''

    #obtain string from tree
    def str(this):
        if this.ch == []:
            return this.c
        s = '(' + this.c
        for t in this.ch:
            s = s + ' ' + t.str()
        return s + ')'

    def leaf(this):
        s = ''
        if this.ch == []:
            s= ' ' + this.c
        for t in this.ch:
            s = s + ' ' + t.leaf()
        return s
    
    def listLeaf(this,n):
        ss = re.split(' +', this.leaf())
        return ss[n]

    def lenLeaf(this):
        ss = re.split(' +', this.leaf())
        return len(ss)
        

    def numCate(this):
        catenum=0
        if this.ch != []:
            catenum = catenum + 1
        for t in this.ch:
            catenum = catenum + t.numCate()
        return catenum

    def numWord(this):
        strnum = 0
        if this.ch == []:
            strnum = strnum + 1
        for t in this.ch:
            strnum = strnum +t.numWord()
        return strnum

        
#line = '( vs ( NS(NS a big cat) with (NS a hat) on it) ( VP sat down (RP on (Ns the bed))))'
#while line != '':
#    t=Tree()
#    line = t.read(line)
#    #print t.str()
#    print t.numCate()
#    print t.numWord()
#    print t.leaf()
#    n = input("Enter your number: ")
#    if n > 0 and n < t.lenLeaf():
#        print t.listLeaf(n)
#    else: print "No such a word"

