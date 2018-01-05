from base64 import b64decode as dec

def f(L):
    iL = [ord(c) for c in L]
    hL = [hex(n)[2:].zfill(2) for n in iL]
    return ''.join(hL)

fn = 'kf'
fh = open(fn)
data = fh.read()
fh.close()

# base64 with newlines
data = ''.join(data.strip().split('\n')[1:-1])
b = dec(data)
bL = b.split('\x02')

# analysis

# n is the 4th item
n = f(bL[3])
# first two bytes are `8181`, repeats the len in hex: 129
print 'n'
print n[4:24], n[-20:]
v = str(eval('0x' + n[4:]))
print v[:20], v[-20:]

for i,e in enumerate(bL):
    # convert to 1-based index
    print str(i+1).rjust(2), f(e)[:40]

d = int('0x' + f(bL[5])[4:], 16)
p = int('0x' + f(bL[6])[4:], 16)
q = int('0x' + f(bL[8])[4:], 16)
print 'd', hex(d)[:20]
print 'p', hex(p)[:20]
print 'q', hex(q)[:20]
print '?', hex(d % (p-1))[:20]
