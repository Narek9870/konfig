import re
import json
import sys
import argparse


class ConfigParser:
    def __init__(self):
        self.variables = {}

    def parse(self, input_stream):
        lines = input_stream.readlines()
        print(f"Прочитано {len(lines)} строк из входных данных.")

        for line in lines:
            line = line.strip()
            print(f"Чтение строки: {line}")

            if not line or line.startswith('#'):
                continue

            if line.startswith('var '):
                self.handle_variable_declaration(line)
            elif line.startswith('list('):
                self.handle_list_declaration(line)
            else:
                print(f"Ошибка: Некорректный синтаксис в строке '{line}'.")

        print("\nКонстанты и данные:")
        print(json.dumps(self.variables, ensure_ascii=False, indent=4))

    def handle_variable_declaration(self, line):
        match = re.match(r'var (\w+) := (.+)', line)
        if match:
            var_name = match.group(1)
            value = self.transform_value(match.group(2))
            if value is None:
                raise Exception(f"Переменная '{var_name}' не найдена.")
            self.variables[var_name] = value
            print(f"Добавлена переменная: {var_name} = {value}")

    def handle_list_declaration(self, line):
        match = re.match(r'list\((.*)\)', line)
        if match:
            items = match.group(1).split(',')
            items = [self.evaluate_expression(self.replace_variables_in_expression(item.strip())) for item in items]
            self.variables['list'] = [self.transform_value(item) if isinstance(item, str) else item for item in items]
            print(f"Добавлен список: {self.variables['list']}")
        else:
            print(f"Ошибка: Некорректный синтаксис в строке '{line}'.")

    def transform_value(self, value):
        value = value.strip()

        # Обработка чисел
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass

        # Обработка строк
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]

        # Обработка логических значений
        elif value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False

        # Обработка переменных
        elif value.startswith('${') and value.endswith('}'):
            var_name = value[2:-1]
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                print(f"Ошибка: Переменная '{var_name}' не найдена.")
                return None

        return value

    def replace_variables_in_expression(self, expression):
        if '${' in expression and '}' in expression:
            variables_in_expression = re.findall(r'\${(\w+)}', expression)
            for var in variables_in_expression:
                if var in self.variables:
                    expression = expression.replace(f'${{{var}}}', str(self.variables[var]))
                else:
                    print(f"Ошибка: Переменная '{var}' не найдена в выражении '{expression}'.")
                    return None
        return expression

    def evaluate_expression(self, expression):
        try:
            expression = self.replace_variables_in_expression(expression)
            if any(op in expression for op in '+-*/'):
                return eval(expression)
            return expression
        except Exception as e:
            print(f"Ошибка при вычислении выражения '{expression}': {e}")
            return expression


def main():
    parser = argparse.ArgumentParser(description="Парсер конфигурационного файла.")
    parser.add_argument('input_file', type=str, help="Путь к файлу конфигурации (.conf)")
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        config_parser = ConfigParser()
        config_parser.parse(f)


if __name__ == "__main__":
    main()
