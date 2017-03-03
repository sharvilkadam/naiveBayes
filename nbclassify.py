import sys
import re
import math

def readText( file1 ):
    fo = open(file1, "r")
    text=fo.read()
    fo.close()
    return text

def writeOutput( str ):
    wo = open("nboutput.txt","w")
    wo.write(str)
    wo.close()
    return

def parsePrior( m ):
    m1 = m.split(" ")
    m11 = m1[0].split("/")
    m12 = math.log(float(m11[0])/float(m11[1]))
    m21 = m1[1].split("/")
    m22 = math.log(float(m21[0]) / float(m21[1]))
    m31 = m1[2].split("/")
    m32 = math.log(float(m31[0]) / float(m31[1]))
    m41 = m1[3].split("/")
    m42 = math.log(float(m41[0]) / float(m41[1]))
    prior = [ m12 , m22 , m32 , m42 ]
    return prior

def parseModel( model ):
    del model[0]
    del model[0]
    del model[0]
    del model[0]
    del model[0]     #removing forst 5 line of the model
    d = dict()
    #print model
    for x in model:
        t = x.split(":")
        p = t[1].strip('\t')
        p1 = p.split(" ")
        m11 = p1[0].split("/")
        m12 = math.log(float(m11[0]) / float(m11[1]))
        m21 = p1[1].split("/")
        m22 = math.log(float(m21[0]) / float(m21[1]))
        m31 = p1[2].split("/")
        m32 = math.log(float(m31[0]) / float(m31[1]))
        m41 = p1[3].split("/")
        m42 = math.log(float(m41[0]) / float(m41[1]))
        d[t[0]] = [ m12 , m22 , m32 , m42 ]

    return d

def classifyLine( line  , d , prior ):
    words = line.split(" ")
    op = words[0] + " "
    #print outputStr
    truth = prior[0]
    decep = prior[1]
    posi = prior[2]
    nega = prior[3]
    for l in words:
        cw0 = l.lower()
        cw = re.findall(r"[\w']+", cw0)
        for w1 in cw:
            if d.has_key(w1):
                pp = d.get(w1)      #pp contains all the partial probabilititis of that feature word
                truth += pp[0]
                decep += pp[1]
                posi += pp[2]
                nega += pp[3]

    if truth > decep:
        op += "truthful"+ " "
    else:
        op += "deceptive" + " "

    if posi > nega:
        op += "positive" + " "
    else:
        op += "negative" + " "
    #print outputStr
    return op


file1 = str(sys.argv[1]) #file path to test.txt
file2 = "nbmodel.txt"
text = readText(file1)
model = readText(file2)
t2 = text.split("\n")     #t2 contains all the test lines
m2 = model.split("\n")      #m2 contains all the lines on the model.txt

prior = parsePrior(m2[1])
#print prior     #dictionanry of priors

d = parseModel(m2)
#print d     #dictionary on partial probabilities

outputStr = ""
count = 0
while count<len(t2):
    if len(t2[count].strip()) !=0:
        o = classifyLine(t2[count] , d , prior)
        outputStr += o
        if count != (len(t2)-1):
            outputStr += "\n"
    count+=1

#print outputStr
writeOutput(outputStr)
