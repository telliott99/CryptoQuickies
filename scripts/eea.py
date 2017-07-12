import sys

'''
gcd(60,13) gives a list of quotients:
[4,1,1,1,1]
our goal is to extract from that list the number 37
13 * 37 = 1 mod 60
'''

# requires a > b
def gcd(a,b):
    r = a % b
    L = [[a,b,a/b,r]]
    while not r == 0:
        a,b = b,r
        r = a % b
        q = a / b
        L.append([a,b,q,r])
    return L  

a = int(sys.argv[1])
b = int(sys.argv[2])
L = gcd(a,b)
#for e in L:
    #print e
L.reverse()

N = len(L)
L.pop(0)    # don't need the last one

# round 1
# define ca as the coefficient of a
# define cb as the coefficient of b

def pp(t):
    print 'a=%d,b=%d,q=%d,r=%d,ca=%d,cb=%d' % t

a,b,q,r = L.pop(0)
ca = 1
cb = -q
t = a,b,q,r,ca,cb
pp(t)

# round 2+
for i in range(2,N):
    a,b,q,r = L.pop(0)
    tmp = ca
    ca = cb
    cb = tmp - q * cb
    t = a,b,q,r,ca,cb
    pp(t)

cb = cb % a

print 'multiplicative inverse of',
print b, 'is', cb, 'mod', a