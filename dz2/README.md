## Клонирование репозитория
Склонируйте репозиторий с исходным кодом и тестами:
git clone https://github.com/Narek9870/konfig
cd konfig


## Запуск
Запуск эмулятора
cd C:\Users\ПК\dependency-visualizer\src
python dependency_visualizer.py -n bash -o output.puml -f C:\Users\ПК\dependency-visualizer\Packages.gz
java -jar plantuml.jar -verbose output.puml

## Структура проекта
Packages.gz
/src
  dependency_visualizer.py
  output.pulm
  plantuml.jar
  test_dependency_visualizer.py
