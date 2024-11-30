## Клонирование репозитория
Склонируйте репозиторий с исходным кодом и тестами:
```bash
git clone https://github.com/Narek9870/konfig
cd konfig
```

## Запуск
Запуск эмулятора
```bash
cd C:\Users\ПК\config_transpiler
python config_parser.py C:\Users\ПК\config_transpiler\examples\example1.conf
```
![image](https://github.com/user-attachments/assets/f59bb928-8bc0-455f-8988-6b90a368760b)
```
python config_parser.py C:\Users\ПК\config_transpiler\examples\example2.conf
```
![image](https://github.com/user-attachments/assets/d59a42ba-5f37-463c-9c83-f2790bb6be71)


```
python config_parser.py C:\Users\ПК\config_transpiler\examples\example3.conf
```
![image](https://github.com/user-attachments/assets/bba9c26c-62b5-4bac-9d39-2ca5f7951271)

```
pytest test_config_parser.py
```
![image](https://github.com/user-attachments/assets/5f8989b6-a896-44a1-8323-93bf878452d4)


## Структура проекта
```bash
/config_transpiler
  config_parser.py
  test_config.sh
  test_config_parser.py
/examples
  example1.conf
  example2.conf
  example3.conf
```

