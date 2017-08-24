def gcd(a, b):
    while b:
        a, b=b, a%b
    return a
def phi(a):
    b=a-1
    c=0
    while b:
        if not gcd(a,b)-1:
            c+=1
        b-=1
    return c
lim = 1000000;
sum = 0;
for i in range(2,lim):
    sum = sum + phi(i);
    if i% 1234 == 0:
        print(i);
print(phi(17));


