#include <stdio.h>
#include <stdlib.h>

int main(){
   char* home=getenv("APPHOME");
       char* cmd=(char*)malloc(strlen(home)+strlen(INITCMD));
       if (cmd) {
               strcpy(cmd,home);
               strcat(cmd,INITCMD);
               execlp(cmd, NULL);
       }
   return 0;
}