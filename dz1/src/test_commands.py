import unittest
from unittest.mock import patch, mock_open
import os
from commands import CommandExecutor


class TestCommandExecutor(unittest.TestCase):

    def setUp(self):
        """Настройка тестового окружения"""
        # Указываем путь к реальной папке test_vfs
        self.vfs_root = os.path.join(os.getcwd(), "test_vfs")

        # Создаем test_vfs, если папка не существует
        if not os.path.exists(self.vfs_root):
            os.makedirs(self.vfs_root)

        # Создаем структуру каталогов и файлов для тестов
        os.makedirs(os.path.join(self.vfs_root, "dir1"), exist_ok=True)
        os.makedirs(os.path.join(self.vfs_root, "dir2"), exist_ok=True)
        os.makedirs(os.path.join(self.vfs_root, "dir3"), exist_ok=True)
        with open(os.path.join(self.vfs_root, "dir1", "file1.txt"), "w") as f:
            f.write("File content")

        # Инициализация экземпляра CommandExecutor с реальным корнем
        self.executor = CommandExecutor(self.vfs_root, "/")

    @patch("sys.stdout")
    def test_ls_root(self, mock_stdout):
        """Тестируем команду ls в корневой директории"""
        # Мокаем вызов os.listdir для текущей директории
        with patch("os.listdir", return_value=["dir1", "dir2", "dir3"]):
            self.executor.ls()
            output = "".join([call[0][0] for call in mock_stdout.write.call_args_list])
            # Проверяем, что вывод содержит папки
            self.assertIn(f"[Dir] dir1", output)
            self.assertIn(f"[Dir] dir2", output)
            self.assertIn(f"[Dir] dir3", output)

    @patch("sys.stdout")
    def test_ls_dir1(self, mock_stdout):
        """Тестируем команду ls в директории dir1"""
        # Мокаем os.listdir для директории /dir1
        with patch("os.listdir", return_value=["file1.txt"]):
            self.executor.current_dir = os.path.join(self.vfs_root, "dir1")  # используем реальный путь
            self.executor.ls()
            output = "".join([call[0][0] for call in mock_stdout.write.call_args_list])
            # Проверяем, что вывод содержит файл
            self.assertIn("file1.txt", output)

    def test_cd_to_existing_directory(self):
        """Тестируем команду cd на переход в существующую директорию"""
        # Мокаем os.path.isdir
        with patch("os.path.isdir", return_value=True):
            self.executor.cd("dir1")
            self.assertEqual(self.executor.current_dir, os.path.join("/", "dir1"))

    def test_cd_to_non_existing_directory(self):
        """Тестируем команду cd на переход в несуществующую директорию"""
        # Мокаем os.path.isdir для несуществующей директории
        with patch("os.path.isdir", return_value=False):
            with patch("sys.stdout") as mock_stdout:
                self.executor.cd("non_existing_dir")
                output = "".join([call[0][0] for call in mock_stdout.write.call_args_list])
                self.assertIn("Error: Directory 'non_existing_dir' does not exist.", output)

    def test_cd_up(self):
        """Тестируем команду cd с переходом на уровень вверх"""
        self.executor.current_dir = os.path.join("/", "dir1")
        self.executor.cd("..")
        self.assertEqual(self.executor.current_dir, "/")


    def test_cat_non_existing_file(self):
        """Тестируем команду cat для несуществующего файла"""
        result = self.executor.cat("non_existing_file.txt")
        self.assertEqual(result, "Error: File 'non_existing_file.txt' does not exist.")

    def tearDown(self):
        """Очистка тестовой среды после выполнения тестов"""
        # Удаляем test_vfs и все его содержимое после тестов
        for root_dir in os.listdir(self.vfs_root):
            dir_path = os.path.join(self.vfs_root, root_dir)
            if os.path.isdir(dir_path):
                for file in os.listdir(dir_path):
                    os.remove(os.path.join(dir_path, file))
                os.rmdir(dir_path)
        os.rmdir(self.vfs_root)


if __name__ == "__main__":
    unittest.main()
