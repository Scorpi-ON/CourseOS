# CourseOS

[![license](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![release](https://img.shields.io/github/v/release/Scorpi-ON/CourseOS?include_prereleases)](https://github.com/Scorpi-ON/CourseOS/releases)
[![downloads](https://img.shields.io/github/downloads/Scorpi-ON/CourseOS/total)](https://github.com/Scorpi-ON/CourseOS/releases)
[![code size](https://img.shields.io/github/languages/code-size/Scorpi-ON/CourseOS.svg)](https://github.com/Scorpi-ON/CourseOS)

[![Ruff and MyPy checks](https://github.com/Scorpi-ON/CourseOS/actions/workflows/linters.yaml/badge.svg)](https://github.com/Scorpi-ON/CourseOS/actions/workflows/linters.yaml)
[![C++ build](https://github.com/Scorpi-ON/CourseOS/actions/workflows/cpp-build.yaml/badge.svg)](https://github.com/Scorpi-ON/CourseOS/actions/workflows/cpp-build.yaml)
[![pytest tests](https://github.com/Scorpi-ON/CourseOS/actions/workflows/tests.yaml/badge.svg)](https://github.com/Scorpi-ON/CourseOS/actions/workflows/tests.yaml)
[![PyQt UI compilation](https://github.com/Scorpi-ON/CourseOS/actions/workflows/ui-compile.yaml/badge.svg)](https://github.com/Scorpi-ON/CourseOS/actions/workflows/ui-compile.yaml)
[![CodeQL (Python, C++, GH Actions)](https://github.com/Scorpi-ON/CourseOS/actions/workflows/codeql.yaml/badge.svg)](https://github.com/Scorpi-ON/CourseOS/actions/workflows/codeql.yaml)

Курсовой проект по операционным системам, продуктом которого является эмулятор файловой системы S5FS, а
также межпроцессного взаимодействия.

<details><summary><h2>Скриншоты</h2></summary>
    <h3>Эмулятор ФС</h3>
    <p>Авторизация:</p>
    <img src="https://github.com/user-attachments/assets/0ef55d55-1c32-474d-ad17-be6081ca5197" width="50%">
    <br>
    <br>
    <p>Списки групп и пользователей:</p>
    <img src="https://github.com/user-attachments/assets/7fc6ad1c-c6c5-46d5-8380-dcad630a4655" width="50%">
    <br>
    <br>
    <p>Список файлов:</p>
    <img src="https://github.com/user-attachments/assets/c4b393c2-7303-4730-8f71-89036be1bbca" width="50%">
    <br>
    <br>
    <p>Создание новой группы:</p>
    <img src="https://github.com/user-attachments/assets/3a15fc15-cb29-4598-8a85-dcef9adbeb45" width="50%">
    <br>
    <br>
    <p>Создание нового пользователя:</p>
    <img src="https://github.com/user-attachments/assets/f0723028-74fb-4cb1-a65f-327ad656fa7b" width="50%">
    <br>
    <br>
    <p>Группа и пользователь успешно добавлены:</p>
    <img src="https://github.com/user-attachments/assets/f7e0489a-a7c5-419d-a5f4-dfe10ba0b5ee" width="50%">
    <br>
    <br>
    <p>Попытка открыть системный файл (запрещено):</p>
    <img src="https://github.com/user-attachments/assets/2de5b047-a9f3-424c-b3dd-148669904e53" width="50%">
    <br>
    <br>
    <p>Подтверждение перед удалением не системного файла:</p>
    <img src="https://github.com/user-attachments/assets/d8c24545-6c41-41e9-9b72-9d1f46e4ee48" width="50%">
    <br>
    <br>
    <p>Поскольку файл был создан другим пользователем, а у других пользователей права на запись нет, удалить его нельзя:</p>
    <img src="https://github.com/user-attachments/assets/2c343b0f-d99c-4215-bd6f-bc8a11964c2e" width="50%">
    <br>
    <br>
    <p>Создание нового файла:</p>
    <img src="https://github.com/user-attachments/assets/b9b25f5e-bd3d-4656-9c9c-fafdbaba5cf2" width="50%">
    <br>
    <br>
    <p>Выставление прав при создании нового файла:</p>
    <img src="https://github.com/user-attachments/assets/993b2eac-3e5d-4d61-a61b-6e9853d4fec6" width="50%">
    <br>
    <br>
    <p>Открытие файла после создания (метаданные обновлены):</p>
    <img src="https://github.com/user-attachments/assets/f9ef2961-3d36-4cf4-af0d-d4bc5460c4ea" width="50%">
    <br>
    <br>
    <p>Открытие файла после снятия права на запись (поля заполнены данными, но не активны для изменения):</p>
    <img src="https://github.com/user-attachments/assets/769736c8-6a63-447c-8629-186c5440240f" width="50%">
    <br>
    <br>
    <p>Дата модификации файла после его редактирования обновлена:</p>
    <img src="https://github.com/user-attachments/assets/04f72c03-13fa-4dc9-bed6-e9e76a38aa84" width="50%">
    <br>
    <br>
    <p>Копирование файла:</p>
    <img src="https://github.com/user-attachments/assets/0b0547a6-fa1f-477d-8dee-c757e625a962" width="50%">
    <br>
    <br>
    <p>Удаление исходного файла (будет произведено только после возвращения права на запись):</p>
    <img src="https://github.com/user-attachments/assets/9e025cba-a86f-4126-93e0-b4bdc47e6f89" width="50%">
    <h3>Демо межпроцессного взаимодействия</h3>
    <p>Каналы:</p>
    <img src="https://github.com/user-attachments/assets/1b261cc0-b4e2-4ca2-9439-0adfd433a221" width="65%">
    <br>
    <br>
    <p>Именованные каналы:</p>
    <img src="https://github.com/user-attachments/assets/edf4465f-1b42-410c-89d7-0876f88fe447" width="65%">
    <br>
    <br>
    <p>Разделяемая память:</p>
    <img src="https://github.com/user-attachments/assets/4fb2e732-fc55-44c9-bb80-667201999360" width="65%">
</details>

## Основные требования

- файловая система должна эмулировать структуру и принцип работы S5FS
- файловая система должна «работать» в бинарном файле
- файловая система должна быть одноуровневой и работать с битовой картой свободных/занятых кластеров
- файловая система должна поддерживать:
    - CRUD-операции с файлами и каталогами
    - создание пользователей и групп, вход в систему от имени пользователей
    - настройку прав доступа к файлам и каталогам
    - дополнительные возможности на усмотрение разработчика
- в прототипе межпроцессного взаимодействия должны быть реализованы следующие средства:
    - каналы
    - именованные каналы
    - разделяемая память
- эмулятор файловой системы должен быть выполнен в виде графического приложения
- работу межпроцессного взаимодействия можно проиллюстрировать в отдельных консольных программах
- язык написания эмулятора ФС — любой, межпроцессного взаимодействия — один из низкоуровневых (например, C/C++)

## Особенности реализации

- [x] все требования соблюдены
- [x] эмулятор файловой системы кроссплатформенный, межпроцессное взаимодействие написано под Linux- [x] операции с бинарным файлом файловой системы покрыты тестами
- [x] интегрированы инструменты управления зависимости и статического анализа кода
- [x] проверка качества кода посредством CI/CD пайплайнов и Git-хуков

## Стек

- **Python** — основной язык программирования
- **uv** — пакетный менеджер
- **pytest** — фреймворк для тестирования
- **Ruff** — инструмент для форматирования и анализа кода
- **MyPy** — статический типизатор Python
- **pre-commit** — фреймворк для настройки хуков Git
- **GNU C++** — компилятор C++ для иллюстрации межпроцессного взаимодействия

## Установка и запуск

### Эмулятор ФС

0. Клонируйте репозиторий и перейдите в папку эмулятора:

```shell
git clone git@github.com:Scorpi-ON/CourseOS.git
cd CourseOS/fs
```

1. Установите пакетный менеджер uv одним из способов. Например, для Windows:

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Установите зависимости:

```shell
uv sync --frozen --no-dev
```

3. Теперь запускать проект можно командой:

```shell
uv run -m CourseOS
```

### Демо межпроцессного взаимодействия

0. Клонируйте репозиторий и перейдите в папку файлов межпроцессного взаимодействия:

```shell
git clone git@github.com:Scorpi-ON/CourseOS.git
cd CourseOS/processes
```

1. Запуск демонстрации работы **каналов**:

```shell
g++ pipes.cpp -o pipes.out && ./pipes.out
```

2. Запуск демонстрации работы **именованных каналов** (выполняется с двух терминалов, открытых параллельно):

Ридер:

```shell
g++ named_pipes_reader.cpp -o named_pipes_reader.out && ./named_pipes_reader.out
```

Райтер:

```shell
g++ named_pipes_writer.cpp -o named_pipes_writer.out && ./named_pipes_writer.out
```

3. Запуск демонстрации работы **разделяемой памяти** (выполняется с двух терминалов, открытых параллельно):

Ридер:

```shell
g++ shared_memory_reader.cpp -o shared_memory_reader.out && ./shared_memory_reader.out
```

Райтер:

```shell
g++ shared_memory_writer.cpp -o shared_memory_writer.out && ./shared_memory_writer.out
```

## Модификация

### Эмулятор ФС

Чтобы модифицировать проект, необходимо установить все зависимости, включая необходимые только для разработки:

```shell
uv sync
pre-commit install --hook-type pre-commit --hook-type pre-push```
```

Запустить форматирование кода, его линтинг и статический анализ типов можно следующими командами соответственно:

```shell
ruff format
ruff check --fix
mypy .
```
Эта операция производятся автоматически при коммитах.

Для запуска всех автотестов выполните команду:

```shell
pytest CourseOS/tests
```

Эта операция производятся автоматически при отправке изменений.
