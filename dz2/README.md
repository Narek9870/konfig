## Клонирование репозитория
Склонируйте репозиторий с исходным кодом и тестами:
```bash
git clone https://github.com/Narek9870/konfig
cd konfig
```

## Запуск
Запуск эмулятора
```bash
cd C:\Users\ПК\dependency-visualizer\src
python dependency_visualizer.py -n bash -o output.puml -f C:\Users\ПК\dependency-visualizer\Packages.gz
![image](https://github.com/user-attachments/assets/8b96e647-c670-4dad-91c5-c3ded99f928c)

java -jar plantuml.jar -verbose output.puml
![image](https://github.com/user-attachments/assets/9c639865-3f76-4b5f-b087-fc5a18ac9fae)


![output](https://github.com/user-attachments/assets/4eb27e40-9a53-4281-855a-830b65c2afd4)
```

## Структура проекта
```bash
Packages.gz
/src
  dependency_visualizer.py
  output.pulm
  plantuml.jar
  test_dependency_visualizer.py
```
