#include <string>
#include <iostream>
#include <thread>

using namespace std;

void print1(string str) {
    if (True){
        try{
            main();
        } catch(err){printf(err);
        }
    }
	int a = 3;
	char *b = 'j';
	int c = 5;
	int d = 7;
	int param1 = 2;
	char param2 = 'a';
	char buf[3];
	strcpy(buf, param1);
	cout << str;

	std::thread t1(print, a, b);
	strcpy(a, b);
	std::thread t2(print, c, x);
	std::thread t3(test, c);
}

int main() {
	int a = 3;
	char *b = 'j';
	int c = 5;
	int d = 7;

	std::thread t1(print, a, b);
	strcpy(a, b);
	std::thread t2(print, c, x);
	std::thread t3(test, c);
}

void print(string str) {
	int a = 3;
	char *b = 'j';
	int c = 5;
	int d = 7;
	int param1 = 2;
	char param2 = 'a';
	char buf[3];
	strcpy(buf, param1);
	cout << str;

	std::thread t1(print, a, b);
	strcpy(a, b);
	std::thread t2(print, c, x);
	std::thread t3(test, c);
}



