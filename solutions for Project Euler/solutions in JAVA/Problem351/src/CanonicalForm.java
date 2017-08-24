import java.util.Iterator;

/**
 * Created by Bar Angel on 3/11/2017.
 */
public class CanonicalForm {
    public static void main(String[] args){
        int lim = 1000; //100000000;
        EratosthenesSieve ers= new EratosthenesSieve(lim*2);

        System.out.println("?");
        long sum = 0;

        int phi;
        for(int i=0;i<=lim;i++){
            phi = fastPhi(i,ers);
            sum += i-phi;
            System.out.println(i + " -> " + phi);
        }
        System.out.println("Answer: " + (int)(6*sum));
    }
    public static int fastPhi(int n, EratosthenesSieve ers){
        int phi = 1;
        int sqrt = (int)Math.sqrt(n) + 1;
        Iterator<Integer> piter = ers.iterator();
        int curp = piter.next();
        while(curp <= n){
            if(n % curp == 0){
                phi *= (degree(curp,n)/curp)*(curp-1);
            }
            curp = piter.next();
        }
        return phi;
    }

    public static int degree(int p, int n){
        int m = p;
        if(n % p != 0)
            return 1;
        while((n/m) % m == 0)
            m *= m;

        return m*degree(p,n/m);
    }
}
