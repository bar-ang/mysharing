#include <iostream>
#include <cmath>
using namespace std;

int main ()
{
   int a;

   try{
   		a = 10;
   		throw a;
   }catch(int res){
   	 cout << res << endl;
   }

   return 0;
}

