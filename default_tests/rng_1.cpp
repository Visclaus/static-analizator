#include <random>

int main () {
   int non_safe_number = srand(300);
   int safe_number;
   for( i = 0 ; i < n ; i++ ) {
      printf("%d\n", rand() % 50);
   }
   safe_number = srand(time());
   std::uniform_real_distribution<double> dist(0.0, 1.0);
   return(0);
}