# note:  uses SystemRandom
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
    help="use digits *only*", 
    action='store_true')
parser.add_argument("-U", 
    help="add uppercase", 
    action='store_true')
parser.add_argument("-u",
    help="use uppercase *only*", 
    action='store_true')
parser.add_argument("-p",
    help="use punctuation", 
    action='store_true')
parser.add_argument("--alpha")

args = parser.parse_args()
N = args.length

if args.alpha:  
    aL = args.alpha

if args.D or args.U:
    if args.D and args.U:
        print "options -D and -U mean *only* that symbol class"
        sys.exit()
    if args.D:    aL = D['dg']
    if args.U:    aL = D['uc']

else:
    aL = D['lc']
    if args.d:    aL += D['dg']
    if args.u:    aL += D['uc']
    if args.p:    aL = D['all']

# ----------------------------

from random import SystemRandom
f = SystemRandom().randrange

iL = [f(len(aL)) for i in range(N)]
L = [aL[j] for j in iL]
print ''.join(L)


