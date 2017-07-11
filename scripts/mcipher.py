lc = 'abcdefghijklmnopqrstuvwxyz'
uc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# multiplicative cipher
def mult_cipher(n):
    rL = list()
    for i,c in enumerate(lc):
        V = ((i + 1) * n) % 26
        C = uc[V]
        rL.append(C)
    return dict(zip(lc,rL))

def is_good_cipher(D):
    return len(set(D.values())) == len(uc)

def display(n,D):
    print n
    kL = sorted(D.keys())
    print ''.join(kL)
    print ''.join([D[k] for k in kL])
    print

dL = list()

for n in range(1,1000):
    D = mult_cipher(n)
    if is_good_cipher(D):
        if not D in dL:
            dL.append(D)
            display(n,D)
