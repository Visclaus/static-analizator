#include <iostream>
#include <string>

int main()
{
    try
    {
        // Здесь мы пишем стейтменты, которые будут генерировать следующее исключение
        throw -1; // типичный стейтмент throw
    }
    catch (int a){

        // Любые исключения типа int, сгенерированные в блоке try выше, обрабатываются здесь
        std::cerr << "We caught an int exception with value: " << a << '\n';
    }
    catch (double){ // мы не указываем имя переменной, так как в этом нет надобности (мы её нигде в блоке не используем)

        // Любые исключения типа double, сгенерированные в блоке try выше, обрабатываются здесь
    }
    catch (const std::string &str){ // ловим исключения по константной ссылке

        // Любые исключения типа std::string, сгенерированные внутри блока try выше, обрабатываются здесь

    }

    std::cout << "Continuing our way!\n";

    return 0;
}