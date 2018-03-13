import math
import operator


PageRank={}
PageRank_New={}
key_value_dict = []
damping_factor=0.55
inlink_dictionary={}
outlink_dictionary={}

def inlink_dictionary_func(textfile):
    with open(textfile) as tf:
        oneline = tf.readlines()
        i = 0
        while i < len(oneline):
            key_value_dict = oneline[i].strip().split(' ')
            inlink_dictionary[key_value_dict[0]] = key_value_dict[1:len(oneline)]
            i = i + 1

def sourcecount():
    i = 0
    for f in inlink_dictionary:
        if not inlink_dictionary.get(f):
            i = i + 1
    print("Sources",i)

def inlinksortandfile():
    InlinkLen = {}
    for page in inlink_dictionary:
        InlinkLen[page]= len(inlink_dictionary.get(page))
    InlinkRanking = sorted(InlinkLen.items(), key=operator.itemgetter(1))
    InlinkRanking.reverse()
    tf = open("InlinksSortedG1.txt", "w")
    i = 0
    while i < len(InlinkRanking):
        tf.write(str(InlinkRanking[i]) + "\n")
        i = i + 1
        if i >= 50:
            break

def numberofvalues(link,keys):
    if link in keys:
        outlink_dictionary[link] = outlink_dictionary[link] + 1
    else:
        outlink_dictionary[link] = 1

def outlink_dictionary_func():
    list(map(lambda p: list(map(lambda link: numberofvalues(link,outlink_dictionary.keys()),inlink_dictionary.get(p))),inlink_dictionary ))

def PageRank_calculation():
    inlink_keys = inlink_dictionary.keys()
    N = len(inlink_keys)
    Sink = inlink_dictionary.keys() - outlink_dictionary.keys()
    print("Sink Pages: ", len(Sink))
    count =0
    perplexity=0
    for page in inlink_keys:
        PageRank[page]=(1.0/N)
    while count <= 4 :
        sinkPR=0
        for page in Sink:
            sinkPR=sinkPR+PageRank[page]
        for page in inlink_keys:
            PageRank_New[page]=(1-damping_factor)/N
            PageRank_New[page] = PageRank_New[page] + damping_factor*sinkPR/N
            for x in inlink_dictionary[page]:
                PageRank_New[page] = PageRank_New[page] + damping_factor * PageRank[x]/(outlink_dictionary[x])
        for page in inlink_keys:
            PageRank[page]=PageRank_New[page]
        PPR = 0
        for page in inlink_keys:
            PPR = PPR + PageRank[page] * math.log(float(PageRank[page]),2)
        if (perplexity != 0):
            print("Perplexity in this iteration "+ str(perplexity))
        last_perplexity = perplexity
        perplexity = math.pow(2, -PPR)
        if math.fabs(last_perplexity - perplexity) >= 1:
                count = 0
        else:
                count += 1
    PageRankFile()

def PageRankFile():
    PageRankSorted = sorted(PageRank.items(), key = operator.itemgetter(1))
    PageRankSorted.reverse()
    tf = open("PageRankG1.txt",'w+')
    i = 0
    for x in PageRankSorted:
        if i < 50:
            tf.write(str(x)+ "\n")
        i = i + 1
    tf.close()

def start():
    inlink_dictionary_func("G1.txt")
    outlink_dictionary_func()
    inlinksortandfile()
    sourcecount()
    PageRank_calculation()

start()