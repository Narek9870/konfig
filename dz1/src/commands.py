import os

class CommandExecutor:
    def __init__(self, vfs_root, current_dir):
        """Инициализация исполнителя команд."""
        self.vfs_root = vfs_root  # Корень виртуальной файловой системы
        self.current_dir = current_dir  # Текущая директория

    def execute(self, command):
        """Выполнение команды."""
        if command.startswith("ls"):
            return self.ls()
        elif command.startswith("cd"):
            new_dir = command.split(" ", 1)[1] if " " in command else ""
            self.cd(new_dir)
            return None  # Изменение директории не требует вывода
        elif command.startswith("cat"):
            file_name = command.split(" ", 1)[1] if " " in command else ""
            return self.cat(file_name)
        elif command == "clear":
            self.clear()
        else:
            return f"Unknown command: {command}"

    def ls(self):
        """Вывод содержимого текущей директории."""
        try:
            # Нормализуем текущую директорию
            current_dir = os.path.normpath(self.current_dir.strip('/')) or "/"
            contents = []

            # Формируем полный путь
            path = os.path.join(self.vfs_root, current_dir)

            if not os.path.exists(path) or not os.path.isdir(path):
                print(f"Error: Directory '{current_dir}' does not exist.")
                return

            # Получаем все элементы директории
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    contents.append(f"[Dir] {item}")
                elif os.path.isfile(item_path):
                    contents.append(item)

            # Печатаем содержимое
            if contents:
                print("\n".join(contents))
            else:
                print(f"No files or directories in '{current_dir}'.")
        except Exception as e:
            print(f"Error accessing directory contents: {e}")

    def cd(self, new_dir):
        """Изменение текущей директории."""
        if not new_dir:
            print("Error: No directory specified.")
            return

        # Запрещаем использовать двойные слэши в пути
        if "//" in new_dir:
            print("Error: Invalid directory path. Double slashes are not allowed.")
            return

        # Запрещаем переход в корень файловой системы
        if new_dir == "/" or new_dir == "\\":
            print("Error: Invalid directory path.")
            return

        # Переход на уровень выше
        if new_dir == "..":
            if self.current_dir == "/":
                print("You are already at the root directory.")
                return
            else:
                # Переход на один уровень вверх в структуре директорий
                self.current_dir = os.path.dirname(self.current_dir)
                if self.current_dir == "":
                    self.current_dir = "/"
                print(f"Current directory: {self.current_dir}")
            return

        # Переход в текущую директорию (cd .)
        if new_dir == ".":
            print("Error: Cannot change to the current directory.")
            return

        # Абсолютный или относительный путь
        if new_dir.startswith("/"):
            target_dir = os.path.join(self.vfs_root, new_dir.lstrip("/"))
        else:
            target_dir = os.path.join(self.vfs_root, self.current_dir.strip("/"), new_dir)

        # Нормализуем путь
        target_dir = os.path.normpath(target_dir)

        if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
            print(f"Error: Directory '{new_dir}' does not exist.")
        else:
            self.current_dir = os.path.relpath(target_dir, self.vfs_root)
            if not self.current_dir.startswith("/"):
                self.current_dir = "/" + self.current_dir
            print(f"Current directory: {self.current_dir}")

    def cat(self, file_name):
        """Вывод содержимого файла."""
        if not file_name:  # Если имя файла не указано
            return "Error: No file name provided."

        # Строим путь к файлу
        file_path = os.path.join(self.vfs_root, self.current_dir.strip("/"), file_name)

        # Проверка существования файла
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return f"Error: File '{file_name}' does not exist."

        # Чтение и возврат содержимого файла
        try:
            with open(file_path, "r") as file:
                return file.read()  # Возвращаем содержимое файла
        except Exception as e:
            return f"Error reading file '{file_name}': {e}"

    def clear(self):
        """Очистка экрана."""
        os.system("cls" if os.name == "nt" else "clear")
