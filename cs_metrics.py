'''
Standardized metrics for code-switching
[1]: https://www.isca-speech.org/archive/Interspeech_2017/pdfs/1429.PDF
[2]: http://amitavadas.com/Pub/CMI.pdf
'''

from collections import Counter
import math
from statistics import stdev, mean

LANG_TAGS = ['EN', 'HI']
OTHER_TAGS = ['UNIV', 'NE','ACRO']

def cmi(x):
    x = x.split()
    c = Counter(x)
    max_wi = c.most_common()[0][1]
    n = len(x)
    u = sum([v for k,v in c.items() if k not in LANG_TAGS])
    if n==u: return 0
    return 100 * (1 - (max_wi/(n-u)))

def mindex(x, k=2):
    x = x.split()
    c = Counter(x)
    total = sum([v for k,v in c.items() if k in LANG_TAGS])
    term = sum([(v/total)**2 for k,v in c.items() if k in LANG_TAGS])
    return (1-term)/((k-1)*term)

def lang_entropy(x, k=2):
    x = x.split()
    c = Counter(x)
    total = sum([v for k,v in c.items() if k in LANG_TAGS])
    terms = [(v/total) for k,v in c.items() if k in LANG_TAGS]
    result = sum([(i*math.log2(i)) for i in terms])
    return -result

def spavg(x, k= 2):

    LANG_TAGS = [tag.lower() for tag in LANG_TAGS]
    OTHER_TAGS = [tag.lower() for tag in OTHER_TAGS]

    x = [el.lower() for el in x]

    if isinstance(x,str):
        x = x.split()

    count = 0 
    mem = None
    for l_i, l_j in zip(x,x[1:]):
        if l_i in OTHER_TAGS:
            continue
        if l_i != l_j:
            count+=1

    return count 


def i_index(x,k=2):

    LANG_TAGS = [tag.lower() for tag in LANG_TAGS]
    OTHER_TAGS = [tag.lower() for tag in OTHER_TAGS]

    x = [el.lower() for el in x]

    if isinstance(x,str):
        x = x.split()

    count = 0 
    mem = None
    for l_i, l_j in zip(x,x[1:]):
        if l_i in OTHER_TAGS:
            continue
        if l_i != l_j:
            count+=1

    return count/(len(x) - 1) 





def burstiness(x):
    x = x.split()
    x = list(filter(lambda a: a not in OTHER_TAGS, x))
    spans = []
    cnt = 0
    prev = x[0]
    for i in x[1:]:
        if i==prev: cnt+=1
        else:
            spans.append(cnt+1)
            cnt=0
        prev = i
    if cnt!=0: spans.append(cnt+1)
    span_std = stdev(spans)
    span_mean = mean(spans)
    return ((span_std - span_mean)/(span_std+span_mean))
