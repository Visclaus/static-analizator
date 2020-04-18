	#include <SQL>

	int main() {
	    std::string sql;
	    std::cin « sql;
	    executeQuery("select * from db where id = 'dasd'")
	    auto connect = SQL::connect(“127.0.0.1”. “123”, “123”);
	    SQL::work W(connect);
	    W.execute(sql);
	}
