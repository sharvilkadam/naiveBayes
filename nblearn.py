import sys
import re

def readText( file1 ):
    fo = open(file1, "r")
    text=fo.read()
    fo.close()
    return text

def readLabel( file2 ):
    fo2 = open(file2, "r")
    labels=fo2.read()
    fo2.close()
    return labels

def learnLine( tx , lx , d , prior ):
    l1=lx.split(" ")[1].strip()
    l2=lx.split(" ")[2].strip()
    #calculating priors
    if (l1 == "deceptive"):
        prior[1] = int(prior[1]) + 1
    else:
        prior[0] = int(prior[0]) + 1
    if (l2 == "positive"):
        prior[2] = int(prior[2]) + 1
    else:
        prior[3] = int(prior[3]) + 1
    tlo=tx.split(" ",1)[1]
    tloop=tlo.split(" ")
    for word in tloop:
        wordlist=cleanWord(word)
        for w1 in wordlist:
            learnWord(w1 , l1 , l2, d)

    return

def cleanWord( word ):          #removing trailing  punctuations, lower case
    word=word.lower()           #regular expression usage
    return re.findall(r"[\w']+", word)

def learnWord( word , l1 , l2 , d):
    if word:
        if d.has_key(word):
            para = d.get(word)
            plist = para.split(",")
            if (l1 == "deceptive"):
                plist[1] = int(plist[1]) + 1
            else:
                plist[0] = int(plist[0]) + 1
            if (l2 == "positive"):
                plist[2] = int(plist[2]) + 1
            else:
                plist[3] = int(plist[3]) + 1
            d[word] = str(plist[0]) + "," + str(plist[1]) + "," + str(plist[2]) + "," + str(plist[3])
        else:
            if (l1 == "deceptive"):
                p1 = 1
                p0 = 0
            else:
                p1 = 0
                p0 = 1
            if (l2 == "positive"):
                p2 = 1
                p3 = 0
            else:
                p2 = 0
                p3 = 1
            d[word] = str(p0) + "," + str(p1) + "," + str(p2) + "," + str(p3)

    return

def smoothenAndCalulateTotal( d ):
    plist = [ 0 , 0 , 0 , 0]
    for key , value in d.iteritems():
        vlist=value.split(",")
        vlist[0] = int(vlist[0]) + 1
        vlist[1] = int(vlist[1]) + 1
        vlist[2] = int(vlist[2]) + 1
        vlist[3] = int(vlist[3]) + 1
        d[key] = str(vlist[0]) + "," + str(vlist[1]) + "," + str(vlist[2]) + "," + str(vlist[3])
        plist[0] = plist[0] + vlist[0]
        plist[1] = plist[1] + vlist[1]
        plist[2] = plist[2] + vlist[2]
        plist[3] = plist[3] + vlist[3]
    return plist

def writeModel( str ):
    wo = open("nbmodel2.txt","w")
    wo.write(str)
    wo.close()
    return

def writeModel2( str ):
    wo = open("nbmodel.txt","w")
    wo.write(str)
    wo.close()
    return

def visualString ( d , plist , prior , count ):
    modelop = "Prior Probabilities [ Truthful , Deceptive , Positive , Negative ]\n"
    modelop += str(prior[0])+"/"+str(count) +" "+ str(prior[1])+"/"+str(count)+" " +str(prior[2])+"/"+str(count) +" "+str(prior[3])+"/"+str(count) + "\n"
    modelop += "\n"
    modelop += "Feature:\tTruthful Deceptive Positive Negative\n"

    for key , value in d.iteritems():
        vlist=value.split(",")
        modelop += "\n"+key+":\t"+vlist[0]+"/"+str(plist[0])+" "+vlist[1]+"/"+str(plist[1])+" "+vlist[2]+"/"+str(plist[2])+" "+vlist[3]+"/"+str(plist[3])
    return modelop


file2 = str(sys.argv[2]) #labels
file1 = str(sys.argv[1]) #text
text = readText(file1)
labels = readLabel(file2)
#print labels
t2=text.split("\n")     #t2 contains all the 1280 reviews
l2=labels.split("\n")   #l2 contains all the 1280 reviews classification
#print l2[0]
#print t2[0]
d={"the":"0,0,0,0"}         #dict will have the key and 4 parameter {true,decep,posi,nega}
#print "Befoer: " + str(d)

#learnLine(t2[0],l2[0],d)
#learnLine("the",l2[0],d)
#print "After: " + str(d)
#spl=.75
count=0
prior = [ 0 , 0 , 0 , 0 ]
while count<(len(t2)-1):
    learnLine(t2[count], l2[count], d , prior)
    count+=1
#print "Prior" + str(prior)+"/"+ str(count)
plist = smoothenAndCalulateTotal(d)
#print plist
modelop = visualString(d,plist, prior,count)
#writeModel( str(d) )
writeModel2( modelop )
