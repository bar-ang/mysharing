def rep(d, n):
    return int((pow(d, n) - 1) / (d - 1));


lim = pow(10, 12);

sum = 1;

d = 2;
n = 3;


alreadyShown = set([]);

while  rep(d,n) < lim:
    rdn = rep(d,n);
    while rdn < lim:
        if rdn in alreadyShown:
            print("dub " + str(rdn));
        else:
            #print(rdn);
            alreadyShown.add(rdn);
            sum = sum + rdn;
        n = n+1;
        rdn = rep(d,n);
    d = d+1;
    n = 3;

print("$\t" + str(sum));