#include <iostream>
#include <string>
#include <unistd.h>


int main() {
    int pipefd[2];
    pipe(pipefd);

    pid_t pid = fork();

    if (pid == -1) {
       	std::cerr << "Ошибка создания дочернего процесса" << std::endl;
       	return 1;
    } else if (pid == 0) {  // Дочерний процесс (читатель)
        // Закрываем конец для записи
        close(pipefd[1]);

        char buffer[256];

        // Читаем данные из канала
        ssize_t bytesRead = read(pipefd[0], buffer, sizeof(buffer) - 1);

        if (bytesRead > 0) {
            buffer[bytesRead] = '\0';
            std::cout << "[ЧИТАТЕЛЬ] Принято из канала: " << buffer << std::endl;
        }

        // Закрываем конец для чтения
        close(pipefd[0]);
    } else { // Родительский процесс (писатель)
        // Закрываем конец для чтения
        close(pipefd[0]);

        std::string data;
        std::cout << "[ПИСАТЕЛЬ] Введите данные: ";
        std::getline(std::cin, data);

        // Записываем данные в канал
        ssize_t bytesWritten = write(pipefd[1], data.c_str(), data.size());

        if (bytesWritten == -1) {
           	std::cerr << "Ошибка при записи в канал" << std::endl;
        } else {
            std::cout << "[ПИСАТЕЛЬ] Записано в канал: " << data << std::endl;
        }

        // Закрываем конец для записи
        close(pipefd[1]);
    }

    return 0;
}
