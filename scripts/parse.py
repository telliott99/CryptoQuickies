import rsa
from binascii import hexlify
from base64 import b64decode as dec

p = 961748941
q = 982451653
n = 944871836856449473  # p*q
e = 65537
d = 8578341116816273

values = [p,q,n,e,d]
names = list('pqned')
D = dict(zip(values,names))

#-------------

priv_key = rsa.PrivateKey(n,e,d,p,q)
s = priv_key.save_pkcs1()
print s
sL = s.strip().split('\n')[1:3]
s = ''.join(sL)
print s
hL = hexlify(dec(s)).strip().split('02')

#-------------

for e in hL[2:]:
    h = e[2:]
    n = int(h,16)
    print str(n).rjust(18), h.rjust(18), 
    if n in D:
        print D[n],
    print
