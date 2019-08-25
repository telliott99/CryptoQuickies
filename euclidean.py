import sys
L = sys.argv[1:]

def f(L):
    a,b = L
    if a < b:
        a,b = b,a
    r = a % b
    s = "a = %3d, b = %3d, r = %3d"
    print(s % (a,b,r))
    if r == 0:
        return b
    return f([b,r])

L = [int(c) for c in L]
print("result: %d" % f(L))
    
