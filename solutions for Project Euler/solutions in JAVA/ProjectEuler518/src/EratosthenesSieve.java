/**
 * Created by Bar Angel on 3/9/2017.
 */

import java.util.BitSet;
import java.util.Iterator;

public class EratosthenesSieve implements Iterable<Integer>{
    private BitSet primes;
    private int limit;
    public EratosthenesSieve(int lim){
        limit = lim;
        primes = new BitSet(lim);
        sieve(lim,2);
    }
    public EratosthenesSieve(int lim, int startWith){
        limit = lim;
        primes = new BitSet(lim);
        sieve(lim,startWith);
    }
    public EratosthenesSieve(int startWith, BitSet startBitSet){
        limit = startBitSet.length();
        primes = (BitSet)startBitSet.clone();
        sieve(limit,startWith);
    }
    private void sieve(int lim, int start){
        primes.flip(2,lim);
        int curr_prime = start;
        int curr_mult = curr_prime * 2;

        while(curr_prime < lim){
            while (curr_mult < lim){
                primes.set(curr_mult,false);
                curr_mult += curr_prime;
            }
            curr_prime = primes.nextSetBit(curr_prime+1);
            if(curr_prime < 0)
                break;
            if(curr_prime < lim/2) {
                curr_mult = curr_prime * 2;
            }
        }
    }

    public boolean isPrime(int n){
        return primes.get(n);
    }

    public int getLimit(){
        return limit;
    }

    @Override
    public Iterator<Integer> iterator() {
        return new BitSetIterator();
    }

    private class BitSetIterator implements Iterator<Integer>{

        private int cursor;
        BitSet primes_pointer;
        public BitSetIterator(){
            primes_pointer = EratosthenesSieve.this.primes;
            cursor = primes_pointer.nextSetBit(0);
        }
        public boolean hasNext(){
            return cursor >= 0;
        }
        public Integer next(){
            int val = cursor;
            cursor = primes_pointer.nextSetBit(cursor+1);
            return val;
        }
    }
}
