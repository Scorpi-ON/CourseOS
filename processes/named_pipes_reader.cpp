#include <iostream>
#include <unistd.h>
#include <fcntl.h>

#define FIFO_NAME "/tmp/myfifo"
#define BUF_SIZE 1024


void readData() {
    // Открытие FIFO на чтение
    int fd = open(FIFO_NAME, O_RDONLY);
    if (fd == -1) {
        perror("Ошибка при открытии FIFO на чтение");
        exit(EXIT_FAILURE);
    }

    // Считывание данных
    char buf[BUF_SIZE];
    ssize_t bytesRead;
    while ((bytesRead = read(fd, buf, BUF_SIZE)) > 0) {
        std::cout << "Данные: " << buf << std::endl;
    }

    // Закрытие FIFO
   	close(fd);
}


int main() {
    readData();

    return 0;
}
