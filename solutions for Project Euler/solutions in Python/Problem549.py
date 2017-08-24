def gen_primes():
    D = {}
    q = 2

    while True:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1


def ord(p, n):
    if n % p != 0:
        return 0;
    m = p * p;
    prev = p;
    k = 1;
    while (n % m == 0):
        prev = m;
        m *= m;
        k = 2*k;
    return k + ord(p, n / prev);

def Harvest(p,k):
    c = 0;
    i = 0;
    while(c < k):
        i = i + p;
        c = c + ord(p,i);
    if(c > k):
        i -= p
    return i;

def Natural_Harvest(n):
    max = -1;
    for i in gen_primes():
        if(i > n):
            break;
        k = ord(i,n);
        h = Harvest(i,k);
        if h >= max:
            max = h;
        break;

    return max;


lim = pow(10,8);

sum = 0;
for i in range(2,lim+1):
    sum = sum + 1; #Natural_Harvest(i);
    if(i % 400903 == 0):
        print(i);
print("~~" + str(sum) + "~~~");
