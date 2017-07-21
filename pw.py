''' 
note:  uses SystemRandom

examples:
> python pw.py
nvhywbxfhckxzjowtmiddbthrnvakv
> python pw.py --length 10
tioxrmlrrv
> python pw.py -d
zgnqob9ihyd3z1hydvzyioi64jzbef
> python pw.py -D
504544876431199841307629495390
> python pw.py -u
yhdFuFhRAGpIHoDlTnoZRATwicEHFa
> python pw.py -U
NHEYZGACWKNDNXDBEPRUVIOKURHHKJ
> python pw.py -U --length 50
DIOCRFSHXYKJKSZXGUFNYACIJZOQEMPCISDFLKMXMGHZVRVNPQ
> python pw.py --alpha abcdefgh
ecdhfaceafcgbbggbhcdhahfbbhabd
>
''' 

import sys, string, argparse

dg = string.digits 
lt = string.letters
lc = string.lowercase
uc = string.uppercase
all = lt + dg + '$#&*_'
D = {'dg':dg, 'both':lt, 'lc':lc,
     'uc':uc, 'all':all}

parser = argparse.ArgumentParser()
parser.add_argument("--length",
    help="length for password",
    type=int,
    default=30)
parser.add_argument("-d", 
    help="add digits", 
    action='store_true')
parser.add_argument("-D", 
    help="use digits only", 
    action='store_true')
parser.add_argument("-U", 
    help="add uppercase", 
    action='store_true')
parser.add_argument("-u",
    help="use uppercase only", 
    action='store_true')
parser.add_argument("--alpha")

args = parser.parse_args()
N = args.length

aL = D['lc']
if args.d:    aL += D['dg']
if args.u:    aL += D['uc']

if args.D:    aL = D['dg']
if args.U:    aL = D['uc']
if args.alpha:  
    aL = args.alpha

# ----------------------------

from random import SystemRandom
f = SystemRandom().randrange

iL = [f(len(aL)) for i in range(N)]
L = [aL[j] for j in iL]
print ''.join(L)


