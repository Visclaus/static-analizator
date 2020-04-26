#include <mysql/mysql.h> 
#include <stdio.h> 

int main(){ 

   MYSQL mysql; 
   MYSQL_ROW row; 
   MYSQL_RES *result; 
    
   unsigned int num_fields; 
   unsigned int i; 

   mysql_init(&mysql); 

      execute("SELECT * FROM my_table where id = 'test'");
      executeQuery("SELECT * FROM my_table where id = \'test\'");
   return 0;
} 

