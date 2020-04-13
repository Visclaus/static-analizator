#include <stdio.h>
#include <stdlib.h>
#include <random>
#include <iostream>

int main () {
   int i, n;
   time_t t;
   
   n = 5;
   
   /* Intializes random number generator */
   srand((unsigned) time(&t));

   /* Print 5 random numbers from 0 to 49 */
   for( i = 0 ; i < n ; i++ ) {
      printf("%d\n", rand() % 50);
   }
   std::random_device rd;
   std::mt19937 mt(rd());
   std::uniform_real_distribution<double> dist(1.0, 10.0);

   for (int i=0; i<16; ++i)
       std::cout << dist(mt) << "\n";
   
   return(0);
}