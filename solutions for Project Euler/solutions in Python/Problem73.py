def gcd(a, b):
    while b:
        a, b=b, a%b
    return a

def floor(a,b):
    return int((a-(a%b))/b);

def ceil(a,b):
    if a%b == 0:
        return int(a/b);
    else:
        return floor(a,b) + 1;

def frange(l,r,d):
    if d%l == 0:
        lb = int(d/l) + 1;
    else:
        lb = ceil(d,l);

    if d%r == 0:
        rb = int(d/r) - 1;
    else:
        rb = floor(d,r);

    return range(lb,rb+1);

lim = 12000

counter = 0;
for i in range(4,lim+1):
    if i % 1000 == 0:
        print(i);
    for j in frange(3,2,i):
        if gcd(i,j) == 1:
            counter = counter + 1;
print(counter);
