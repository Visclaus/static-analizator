#include <mysql/mysql.h>
#include <stdio.h>

	int main(){
	 mysql_init(&mysql);
	 mysql.executeQuery("smth'");
     if (!mysql_real_connect(&mysql,"localhost","root","","MyDatabase",0,NULL,0))
	   {
	      fprintf(stderr, "Failed to connect to database: Error: %s\n",
	      mysql_error(&mysql));
       }

	   return 0;

	}