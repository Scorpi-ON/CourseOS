#include <iostream>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#define FIFO_NAME "/tmp/myfifo"
#define BUF_SIZE 1024


void sendData() {
    // Открытие FIFO на запись
    int fd = open(FIFO_NAME, O_WRONLY);
    if (fd == -1) {
        perror("Ошибка при открытии FIFO на запись");
        exit(EXIT_FAILURE);
    }

    // Отправка данных
    std::string data;
    std::cout << "Введите данные для отправки (для выхода введите пустую строку): ";
    while (std::getline(std::cin, data) && !data.empty()) {
        write(fd, data.c_str(), data.size() + 1);
        std::cout << "Данные отправлены." << std::endl;
    }

    // Закрытие FIFO
    close(fd);
}

int main() {
	unlink(FIFO_NAME);
	// Создание FIFO
    int res = mkfifo(FIFO_NAME, 0666);

    if (res == -1) {
        perror("Ошибка при создании FIFO");
        exit(EXIT_FAILURE);
    }

    sendData();

    // Удаление FIFO
    unlink(FIFO_NAME);
    
    return 0;
}
