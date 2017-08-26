import java.util.Iterator;

/**
 * Created by Bar Angel on 3/11/2017.
 */
public class Main {
    public static void main(String[] args){
        int lim = 100000000;
        EratosthenesSieve ers = new EratosthenesSieve(lim);

        Iterator<Integer> it1,it2,it3;
        int sum = 0;
        it1 = ers.iterator();
        it2 = ers.iterator();
        it3 = ers.iterator();

        /*
        int v1,v2,v3;
        while (it1.hasNext()) {
            v1 = it1.next();
            while (it2.hasNext()) {
                v2 = it2.next();
                while (it3.hasNext()) {
                    v3 = it3.next();
                    System.out.println(v1 + " " + v2 + " " + v3);
                }
            }
        }
        */
        System.out.println("?");
        for (int v1 : ers){
           // for (int v2 : ers){
               //for (int v3 : ers){
                    //System.out.println(v1 + " " + v2 + " " + v3);
                //}
          //  }
        }
        System.out.println("!");
    }
}
