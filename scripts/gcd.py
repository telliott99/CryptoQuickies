def gcd(a,b):
    while True:
        r = a % b
        if r == 0:
            return b
        a,b = b,r

print gcd(421,111)  # 1
print gcd(60,24)    # 12
print gcd(11838*2888, 99991987*2888) # 2888

def my_gcd(a,b):
    rL = list()
    while b != 0:
        q = a / b
        r = a % b
        rL.append([a,q,b,r])
        a,b = b,r
    return rL

L = my_gcd(53,10)
for sL in L:
    print '%2d = %2d * %2d + %2d' % tuple(sL)
    
'''
53 =  5 * 10 +  3
10 =  3 *  3 +  1
 3 =  3 *  1 +  0
'''


