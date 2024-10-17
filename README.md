<div align="center">
    <h1 align="center">csti</h1>
    <h3>Отправляйте задачи за одну команду.</h3>
</div>

<br/>

Унифицированный интерфейс командной строки для взаимодействия с контест системами.

## Поддерживаемые системы

- **Contest solutions**: не протестировано
- **Ejudge**: поддерживаемая версия для ВМК 2 курс

## Быстрый старт

### Установка 

Nix - пакетный менеджер, с возможностью создания дев шеллов, и установки программ на прямую с github.

### 1. Установка Nix

Linux:
```shell
sudo $ sh <(curl -L https://nixos.org/nix/install) --daemon
```
MacOS:
```shell
sh <(curl -L https://nixos.org/nix/install)
```

Подробности смотреть на [офф. странице nixos][https://nixos.org/download/#nix-install-linux]

### 2. Подключение nix flakes
```shell
sudo echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf
```

### Установка csti
Исполнение следующих комманд следует делать в директории где вы будете решать контесты(или перенесите фалйы flake.nix и flake.lock в необходимую директорию).

```shell
nix flake init -t github:Gadzet005/csti#c-template # Получаем шаблон дев шела.
nix flake update # Обновления(необходимо при первом запуске).
nix develop # Запуск дев шела.
```

Для любителей fish/zsh и прочих шелов, рекомендую использовать комманду ```nix develop -c shell```, либо отредактировать "flake.nix".

## Настройка

```shell

```
