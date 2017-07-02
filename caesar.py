lc = 'abcdefghijklmnopqrstuvwxyz'
uc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Caesar cipher

def caesar(n):
    m = len(lc)
    D = dict()
    for i,c in enumerate(lc):
        j = (i + n) % m
        D[c] = uc[j]
    return D
        
def display(name,D):
    print name
    kL = sorted(D.keys())
    print ''.join(kL)
    print ''.join([D[k] for k in kL])
    print

C3 = caesar(3)
display('C3',C3)

rot13 = caesar(13)
display('rot13',rot13)

s = 'and you too, brutus'
print s
for c in [' ',',']:
    C3[c] = c
print ''.join([C3[c] for c in s])
