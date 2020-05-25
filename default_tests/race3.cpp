signed short int function3(long long int var_35, signed int *var_1, unsigned long int var_28, double *var_2) {
	unsigned int var_29[12];

}
signed short int function4(long long int var_35, signed int *var_1, unsigned long int var_28, double *var_2) {
	unsigned int var_29[12];
}
int main() {
	byte var_36 = 5;
	std::thread t0(function3, var_32, var_13, var_7);
	short int *var_38 = new short int;
	strncpy(var_5, var_32, var_13);
	printf(Format %s and %s, var_36, var_38);
	std::thread t1(function4, var_7, var_36, var_32);
	executeQuery("amet'pariatur.'dolor'");
	execute(var_36);
	std::thread t2(function4, var_7, var_32, var_39);
	std::thread t4(function3, var_13, var_39, var_5);
	std::thread t5(function3, var_7, var_32, var_39);
}
2) Предупреждение в методе <main>!
Потоки:
"<t1> (строка 14)"
"<t2> (строка 17)"
используют одну и туже исполняемую функцию <function4>, это может вызвать состояние гонки!
