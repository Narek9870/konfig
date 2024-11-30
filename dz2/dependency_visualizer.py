import argparse
import gzip
from collections import defaultdict

def parse_packages_data(packages_data):
    """
    Parse the Packages data and extract package information.

    Args:
        packages_data (str): The content of the Packages file.

    Returns:
        dict: A dictionary mapping package names to their dependencies.
    """
    packages_info = {}
    current_package = {}
    for line in packages_data.split('\n'):
        if line.strip() == '':
            if 'Package' in current_package:
                package_name = current_package['Package']
                depends = current_package.get('Depends', '')
                depends = [dep.strip().split(' ')[0] for dep in depends.split(',')] if depends else []
                packages_info[package_name] = depends
            current_package = {}
        else:
            if ':' in line:
                key, value = line.split(':', 1)
                current_package[key.strip()] = value.strip()
    return packages_info

def build_dependency_graph(package_name, packages_info):
    """
    Build the dependency graph for the given package.

    Args:
        package_name (str): The name of the package to analyze.
        packages_info (dict): A dictionary mapping package names to their dependencies.

    Returns:
        dict: A dictionary representing the dependency graph.

    Raises:
        Exception: If the package is not found in the packages_info.
    """
    if package_name not in packages_info:
        raise Exception(f"Package {package_name} not found in repository.")

    graph = defaultdict(set)
    visited = set()

    def dfs(pkg):
        if pkg in visited:
            return
        visited.add(pkg)
        graph[pkg]  # Ensure the package is added to the graph even if it has no dependencies
        dependencies = packages_info.get(pkg, [])
        for dep in dependencies:
            graph[pkg].add(dep)
            dfs(dep)

    dfs(package_name)
    return graph


def generate_plantuml_code(graph):
    """
    Generate PlantUML code from the dependency graph in component diagram format.

    Args:
        graph (dict): The dependency graph.

    Returns:
        str: The PlantUML code representing the dependency graph.
    """
    lines = ['@startuml']

    # Сортировка пакетов по имени и добавление классов
    for pkg in sorted(graph.keys()):
        # Добавляем кавычки для всех имен с дефисами или пробелами
        pkg_str = f'"{pkg}"' if '-' in pkg or ' ' in pkg else pkg
        lines.append(f'class {pkg_str} {{}}')

    # Добавление зависимостей, исключая самозависимости
    for pkg, deps in graph.items():
        for dep in sorted(deps):
            # Добавляем стрелку, только если зависимость не указывает на сам пакет
            if pkg != dep:
                # Форматируем зависимости с кавычками, если нужно
                pkg_str = f'"{pkg}"' if '-' in pkg or ' ' in pkg else pkg
                dep_str = f'"{dep}"' if '-' in dep or ' ' in dep else dep
                # Добавляем зависимость в граф
                lines.append(f'{pkg_str} --> {dep_str}')

    lines.append('@enduml')
    return '\n'.join(lines)














def main():
    parser = argparse.ArgumentParser(description='Visualize package dependencies in PlantUML format.')
    parser.add_argument('-n', '--name', help='Name of the package to analyze.', required=True)
    parser.add_argument('-o', '--output', help='Path to the output file.', required=True)
    parser.add_argument('-f', '--file', help='Path to the local Packages.gz file.', required=True)
    args = parser.parse_args()

    # Read and decompress the local Packages.gz file
    try:
        with gzip.open(args.file, 'rt', encoding='utf-8') as f:
            packages_data = f.read()
    except Exception as e:
        print(f"Error reading Packages.gz file: {e}")
        return

    # Parse the package data
    packages_info = parse_packages_data(packages_data)

    # Build the dependency graph
    try:
        graph = build_dependency_graph(args.name, packages_info)
    except Exception as e:
        print(f"Error building dependency graph: {e}")
        return

    # Generate PlantUML code from the graph
    plantuml_code = generate_plantuml_code(graph)

    # Output the PlantUML code to the screen
    print(plantuml_code)

    # Write the PlantUML code to the output file
    try:
        with open(args.output, 'w') as f:
            f.write(plantuml_code)
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == '__main__':
    main()
