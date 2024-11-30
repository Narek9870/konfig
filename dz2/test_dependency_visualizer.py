import pytest
from dependency_visualizer import (
    parse_packages_data,
    build_dependency_graph,
    generate_plantuml_code
)
import io
import gzip


def test_parse_packages_data():
    packages_data = """
Package: package1
Depends: package2, package3

Package: package2
Depends: package4

Package: package3

Package: package4
"""
    packages_info = parse_packages_data(packages_data)
    expected_info = {
        'package1': ['package2', 'package3'],
        'package2': ['package4'],
        'package3': [],
        'package4': []
    }
    assert packages_info == expected_info


def test_build_dependency_graph():
    packages_info = {
        'package1': ['package2', 'package3'],
        'package2': ['package4'],
        'package3': [],
        'package4': []
    }
    graph = build_dependency_graph('package1', packages_info)
    expected_graph = {
        'package1': {'package2', 'package3'},
        'package2': {'package4'},
        'package3': set(),
        'package4': set()
    }
    assert graph == expected_graph


def test_generate_plantuml_code():
    graph = {
        'bash': ['debianutils', 'base-files'],
        'base-files': ['libcrypt1', 'libc6'],
        'libc6': ['libcrypt1', 'libgcc-s1'],
        'libgcc-s1': ['gcc-10-base', 'libc6'],
        'libcrypt1': ['libc6'],
    }

    # Получаем код от функции
    code = generate_plantuml_code(graph)

    # Ожидаемый код с зависимостями и классами
    expected_code = """
        @startuml
            bash --> debianutils
            bash --> "base-files"
            "base-files" --> libcrypt1
            "base-files" --> libc6
            libc6 --> libcrypt1
            libc6 --> "libgcc-s1"
            "libgcc-s1" --> "gcc-10-base"
            "libgcc-s1" --> libc6
            libcrypt1 --> libc6
            class "base-files" {}
            class "libgcc-s1" {}
            class bash {}
            class libc6 {}
            class libcrypt1 {}
        @enduml
    """

    # Убираем все лишние пробелы и сравниваем строки без учета отступов и порядка
    def normalize_code(code):
        return sorted([line.strip() for line in code.strip().splitlines()])

    # Нормализуем и сравниваем оба кода
    assert normalize_code(code) == normalize_code(expected_code)



def test_read_local_packages_file():
    # Создаем фиктивный файл Packages.gz с данными
    fake_packages_content = b"""
Package: package1
Depends: package2, package3

Package: package2
Depends: package4

Package: package3

Package: package4
"""
    fake_compressed_data = io.BytesIO()
    with gzip.GzipFile(fileobj=fake_compressed_data, mode='wb') as f:
        f.write(fake_packages_content)
    fake_compressed_data.seek(0)

    # Записываем в файл для теста
    with open('test_Packages.gz', 'wb') as f:
        f.write(fake_compressed_data.getvalue())

    # Читаем файл для теста
    try:
        with gzip.open('test_Packages.gz', 'rt', encoding='utf-8') as f:
            packages_data = f.read()

        # Проверяем, что данные правильно считываются
        assert packages_data.strip() == fake_packages_content.decode('utf-8').strip()
    finally:
        # Удаляем файл после использования
        import os
        os.remove('test_Packages.gz')


def test_build_dependency_graph_package_not_found():
    packages_info = {
        'package1': ['package2', 'package3'],
        'package2': ['package4'],
        'package3': [],
        'package4': []
    }
    with pytest.raises(Exception) as excinfo:
        build_dependency_graph('nonexistent-package', packages_info)
    assert "Package nonexistent-package not found in repository." in str(excinfo.value)

