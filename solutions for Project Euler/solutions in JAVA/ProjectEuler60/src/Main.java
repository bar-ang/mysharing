import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.TreeSet;

/**
 * Created by Bar Angel on 3/14/2017.
 */
public class Main {
    public static void main(String[] args){
        Set<Set<Integer>> ppss = new HashSet<>();
        int lim = Integer.MAX_VALUE/12;
        System.out.println("Sieveing until " + lim);
        EratosthenesSieve ers = new EratosthenesSieve(lim);

        System.out.println("Finish sieveing");

        ers.setAsNotPrime(2);
        ers.setAsNotPrime(5);

        boolean check = findAllPrimePairSets(3, 1000, ers, ppss);
        System.out.println(ppss);
    }


    private static boolean findAllPrimePairSets(int size, int giveup, EratosthenesSieve ers, Set<Set<Integer>> ppss){
        if(size == 1){
            for(int i=2;i<giveup;i++) {
                Set<Integer> iSet = new TreeSet<Integer>();
                iSet.add(i);
                ppss.add(iSet);
            }
            return true;
        }
        Set<Set<Integer>> smaller_ppss = new HashSet<>();
        if(!findAllPrimePairSets(size-1,giveup,ers,smaller_ppss))
            return  false;

        Set<Integer> mergedLeft = new TreeSet<>();
        Set<Integer> mergedRight = new TreeSet<>();
        for(Set<Integer> s : smaller_ppss){
            for(Set<Integer> t : smaller_ppss){
                mergedLeft.clear();
                mergedRight.clear();
                if(mergePPS(s,t,mergedLeft,mergedRight,ers)){
                    if(mergedLeft.size() >= size)
                        ppss.add(new TreeSet<>(mergedLeft));
                    if(mergedRight.size() >= size)
                        ppss.add(new TreeSet<>(mergedRight));
                }
            }
        }

        return ppss.isEmpty();
    }

    public static boolean mergePPS(Set<Integer> s, Set<Integer> t, Set<Integer> mergedLeft, Set<Integer> mergedRight , EratosthenesSieve ers){
        Set<Integer> mergeOnS = new TreeSet<>(s);
        Set<Integer> mergeOnT = new TreeSet<>(t);
        for(int a : t){
            if(!s.contains(a)){
                mergeOnS.add(a);
                if(!isPrimePair(mergeOnS,ers))
                    mergeOnS.remove(a);
            }
        }
        for(int a : s){
            if(!t.contains(a)){
                mergeOnT.add(a);
                if(!isPrimePair(mergeOnT,ers))
                    mergeOnT.remove(a);
            }
        }

        mergedLeft.addAll(mergeOnS);
        mergedRight.addAll(mergeOnT);

        return mergedLeft.size() > s.size() || mergedRight.size() > t.size();
    }



    private static boolean isPrimePair(Set<Integer> primes, EratosthenesSieve ers){
        int con;
        int cat;
        for (int p1 : primes) {
            cat = cat(p1);
            for (int p2 : primes) {
                con = p2*cat+p1;
                if (p1 != p2 && !ers.isPrime(con))
                    return false;
                if (con >= ers.getLimit()) {
                    System.out.println("Did not sieve enough primes." +
                            " Tried to access " + con + " which is larger than " + ers.getLimit());
                    return false;
                }
            }
        }
        return true;
    }

    private static int cat(int b){
        int pow = 1;
        while(pow < b)
            pow *= 10;
        return pow;
    }
}

/*

    private static boolean findPrimePairSet(int size, int giveup, EratosthenesSieve ers, Set<Integer> pps){
        if(size == 0){
            return isPrimePair(pps,ers);
        }

        boolean res;
        for(int i : ers){
            if(i >= giveup)
                break;

            pps.add(i);
            res = findPrimePairSet(size-1,i,ers,pps);
            if(res) {
                System.out.println(pps);
                return  true;
            }


            pps.remove(i);

        }
        return false;
    }

    */