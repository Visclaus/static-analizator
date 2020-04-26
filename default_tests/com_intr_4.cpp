#include <stdio.h>

int main()
{
   char* home=getenv("APPHOME");
    ShellExecute(NULL, _T("open"), _T("C:\\Windows\\Sys32\\sigverif.exe"), NULL, NULL, SW_RESTORE);
   return 0;
}