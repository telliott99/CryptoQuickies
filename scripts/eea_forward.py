import sys
a = int(sys.argv[1])
b = int(sys.argv[2])
if b > a:
    a,b = b,a
o = a,b

s = 0
t = 1

# round 0
q = a / b
r = a % b
x = 1
y = -q

print 'x',x,'y',y

while r != 0:
    a,b = b,r
    q = a / b
    r = a % b
    tmp = x,y
    x = s - q*x
    y = t - q*y
    s,t = tmp
    print 'x',x,'y',y,'s',s,'t',t

print t, 'is the inverse of', o[1], 'mod', o[0]