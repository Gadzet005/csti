<div align="center">
    <h1 align="center">Csti</h1>
    <h3>Отправляйте задачи одной командой.</h3>
</div>

<br/>

Унифицированный интерфейс командной строки для взаимодействия с контест системами.

## Поддерживаемые системы

- **Contest solutions**: не протестировано
- **Ejudge**: поддерживаемая версия для ВМК 2 курс

## Быстрый старт

Взаимодействие с апдейтами/установкой программы происходит через nix, в целом, программу можно собрать из исходников([poetry](https://python-poetry.org/docs/)), но мы не рекомендуем этого делать, потому что появятся затрудниния с установкой зависимостей(gnumake, clang-format, w3m, gcc) и обновлением программы. Поэтому далее будет разобран вариант установки и использования при помощи пакетного менеджера Nix.

### 1. Установка Nix
Nix - пакетный менеджер, с возможностью создания дев шеллов, и установой программ на прямую с github.


Linux:
```shell
sudo $ sh <(curl -L https://nixos.org/nix/install) --daemon
```
MacOS:
```shell
sh <(curl -L https://nixos.org/nix/install)
```

Подробности смотреть на [офф. странице nixos](https://nixos.org/download/#nix-install-linux)

### 2. Подключение nix flakes
```shell
sudo echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf
```

### Установка csti
Исполнение следующих комманд следует делать в директории где вы будете решать контесты(или перенесите файлы flake.nix, flake.lock и ".csti" в необходимую директорию). 

Рекомендация: Дириктория должна быть выделена только под решение контестов.

```shell
nix flake init -t github:Gadzet005/csti#c-template # Получаем шаблон дев шела.
nix flake update # Обновления(необходимо при первом запуске).
nix develop # Запуск дев шела.
```

> ```nix develop``` необходимо делать при каждой новой сессии терминала.


> Для любителей fish/zsh и прочих шелов, рекомендую использовать комманду ```nix develop -c shell_name```, либо отредактировать "flake.nix".

### Первый запуск

Запускаемся в dev shell и инициализируем директорию для работы с контестом.

```shell
nix develop
csti init
```

### Пример использования программы(более подробное объяснение приложено ниже)
```
csti contest select # Выбираем контест, который будем решать, например 7ой.
# Сохраняем файл с задачей(например ./contest7/task2.c)
csti task send # Автоматически отправит 2уй задачу 7ого контеста.
```

## Настройка

```shell
csti configure -g
```

### Организация хранилища

Csti автоматически создает директорию контеста и шаблонны файлов с задачами после комманды ```csti contest select```.

"#" в названии паттернов имен отвечает, за место, где будет расположен порядковый номер.

- Директория архивации: место куда/откуда будут архивироваться/разархивироваться контест после ```csti contest select```, значение "./" - контесты не архивируются.
- Директория выбранного контеста: название папочки с контестом.
- Шаблон названия задач: очевидно!

Пример организации файлов(по умолчанию):
```
.
├── contest6
│   ├── task1.c
│   ├── task2.c
│   ├── task3.c
│   ├── task4.c
│   └── task5.c
├── contest7
│   ├── task1.c
│   ├── task2.c
│   ├── task3.c
│   ├── task4.c
│   └── task5.c
├── flake.lock
└── flake.nix
```

### Доп. функции
Все необходимые зависимости атоматически ставятся при запуске дев шела(clang-format, make, w3m)

- Авто выбор последней сохраненной задачи: csti автоматически сканирует директорию выбранного контеста и выбирает последний сохраненный файла, как задачу.
- Авто тесты: не поддерживается в Ejudge, требует установленного gcc.
- Авто форматирование: перед отправкой задача будет автоматически форматироваться в соответствии с код-стайлом, необходим clang-format.


## Краткий гид по коммандам

```shell
csti init # Инициализирует дирикторию для работы с контестом.
csti configure # Настраивает локальный конфиг(который генерируется с csti init). С флагом "-g", настраивает глобальный конфиг.

# Contest
csti contest info # Информация о выбраном контесте.
csti contest select # Выбрать контест.

# Task
csti task info # Показать всю информацию о задаче.
csti task info -c | w3m -T text/html # Вывести условие задачи в консольный браузер w3m.
csti task select # Выбрать задачу, работает только при отключенном авто выборе.
csti task send # Отправить задачу на проверку.
```

У всех подкоманд task можно передать параметр id(опционально), и тогда будет производиться оперция не с выбранной задачей, а с задачей с указанным id. Аналогично ```csti contest select id```.

Примеры:
```shell
csti task info 5 # Выведет информацию о 5ой задаче выбранного контеста
csti contest select 6 # Выберет 6ой контест.
```

Также у каждой из подкоманд свой ```--help```, там более детальная информация о коммандах.

Примеры:
```shell
csti task --help
csti task info --help 
csti contest select --help
```

## Забавные цитаты во время разработки.
1. "Первый комит: 'initial'. Второй комит: 'remove rust; add python'" - история комитов.
2. "Я такого говнокода навалил, сорян. Но оно работает! А contestEnv тебе все равно не нравится." - senior pomidor developer
3. "Вот если сейчас встану, то за csti больше не сяду, пока у файла main не будет приписки .rs" - 2dChan
4.  Знакомый: "Да ладно на README +-1 час нужен, а ты его откладываешь уже на неделю!"
    
    POV Я в час ночи: "Ну... В целом, 4 часа находится в эпсилон окрестности 1 часа."

5. "Сам открыл пул реквест, сам написал код, сам отревьювил, сам закрыл пул реквест" - я и моя шиза.
