#include <stdio.h>
int main()
{
    SHSTDAPI SHGetFolderPathAndSubDirA(_Reserved_ HWND hwnd, _In_ int csidl, _In_opt_ HANDLE hToken, _In_ DWORD dwFlags, _In_opt_ LPCSTR pszSubDir, _Out_writes_(MAX_PATH) LPSTR pszPath);
	return 0;
}