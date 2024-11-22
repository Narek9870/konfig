## Клонирование репозитория
Склонируйте репозиторий с исходным кодом и тестами:
```bash
git clone https://github.com/Narek9870/konfig
cd konfig
```

## Запуск
Запуск эмулятора
```bash
cd src/emulator-shell-os
python shell_emulator.py --username admin --vfs ../virtual_files.zip --log ../session_log.csv
```

## Структура проекта
```bash
/src
  shell_emulator.py
  commands.py
  test_commands.py
config.csv
session_log.csv
virtual_files.zip
```
