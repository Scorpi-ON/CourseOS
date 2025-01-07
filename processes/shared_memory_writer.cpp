#include <iostream>
#include <unistd.h>
#include <sys/shm.h>

int main() {
    while (true) {
        // Получение идентификатора разделяемой памяти
        int shmid = shmget(1234, sizeof(int), 0666);
        if (shmid == -1) {
            std::cerr << "Ошибка при получении идентификатора разделяемой памяти!" << std::endl;
            return 1;
        }

        // Присоединение разделяемой памяти
        int *data = (int*) shmat(shmid, nullptr, 0);
        if (data == (int*)-1) {
            std::cerr << "Ошибка при присоединении разделяемой памяти!" << std::endl;
            return 1;
        }

        // Ввод данных, которые требуется отправить
        std::cout << "Введите данные для отправки: ";
        int value;
        std::cin >> value;

        // Запись данных в разделяемую память
        *data = value;

        // Отсоединение разделяемой памяти
        if (shmdt(data) == -1) {
            std::cerr << "Ошибка при отсоединении разделяемой памяти!" << std::endl;
            return 1;
        }
    }

    return 0;
}
