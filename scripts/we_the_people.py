alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
fn = 'constitution_preamble.txt'
fh = open(fn)
data = fh.read()
fh.close()
data = data.upper()
L = [c for c in data if c in alpha]
text = ''.join(L[:256])

def f(m, k, mode='enc'):
    n = len(alpha)
    i = alpha.index(m)
    j = alpha.index(k)
    if mode == 'enc':
        i += j
        i %= n
    elif mode == 'dec':
        i -= j
        if i < 0:
            i += n
    else:
        raise ModeError
    return alpha[i]

def test():
    msg = 'ATTACKATDAWN'
    key = text[:len(msg)]
    print msg
    print key
    ctxt = ''.join([f(m,k) for m,k in zip(msg,key)])
    print ctxt
    L = [f(c,k,mode='dec') for c,k in zip(ctxt,key)]
    print ''.join(L)
    
def transpose(txt):
    L = list()
    delta = 16
    for i in range(0,len(txt),delta):
        sL = list(text[i:i+delta])
        L.append(sL)
    tL = zip(*L)
    for pL in tL:
        print ''.join(pL)

if __name__ == "__main__":
    #test()
    transpose(text)