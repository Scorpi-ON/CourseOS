#include <iostream>
#include <sys/shm.h>
#include <unistd.h>

int main() {
    // Создание идентификатора разделяемой памяти
    int shmid = shmget(1234, sizeof(int), IPC_CREAT | 0666);
    if (shmid == -1) {
        std::cerr << "Ошибка при создании идентификатора разделяемой памяти!" << std::endl;
        return 1;
    }

    // Присоединение отображаемой памяти
    int *data = (int*)shmat(shmid, nullptr, 0);
    if (data == (int*)-1) {
        std::cerr << "Ошибка при присоединении разделяемой памяти!" << std::endl;
        // Удаление shared memory
        shmctl(shmid, IPC_RMID, nullptr);
        return 1;
    }

    int prev_data = *data;

    // Чтение данных из отображаемой памяти в бесконечном цикле
    while (true) {
        if (prev_data != *data) {
            std::cout << "Полученные данные: " << *data << std::endl;
            prev_data = *data;
        }
    }

    // Отсоединение отображаемой памяти
    if (shmdt(data) == -1) {
        std::cerr << "Ошибка при отсоединении разделяемой памяти!" << std::endl;
        // Удаление shared memory
        shmctl(shmid, IPC_RMID, nullptr);
        return 1;
    }

    // Удаление shared memory
    if (shmctl(shmid, IPC_RMID, nullptr) == -1) {
        std::cerr << "Ошибка при удалении разделяемой памяти!" << std::endl;
        return 1;
    }

    return 0;
}
