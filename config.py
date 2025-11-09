import os
import toml
from typing import Dict, Any
from errors import *


class DependencyVisualizerConfig:
    def __init__(self, config_path: str = "config.toml"):
        self.config_path = config_path
        self.package_name = ""
        self.repository_url = ""
        self.test_mode = False
        self.local_path = ""
        self._load_config()

    def _load_config(self) -> None:
        """Загрузка конфигурации из TOML файла"""
        try:
            if not os.path.exists(self.config_path):
                raise ConfigFileError(f"Конфигурационный файл не найден: {self.config_path}")

            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = toml.load(f)

            self._validate_and_set_config(config_data)

        except toml.TomlDecodeError as e:
            raise ConfigFileError(f"Ошибка парсинга TOML файла: {e}")
        except Exception as e:
            raise ConfigFileError(f"Неожиданная ошибка при чтении конфигурации: {e}")

    def _validate_and_set_config(self, config_data: Dict[str, Any]) -> None:
        """Валидация и установка параметров конфигурации"""

        # Валидация имени пакета
        if 'package' not in config_data or 'name' not in config_data['package']:
            raise PackageNameError("Отсутствует секция 'package.name' в конфигурации")

        package_name = config_data['package']['name']
        if not package_name or not isinstance(package_name, str):
            raise PackageNameError("Имя пакета должно быть непустой строкой")
        self.package_name = package_name

        # Валидация репозитория
        if 'repository' not in config_data:
            raise RepositoryURLError("Отсутствует секция 'repository' в конфигурации")

        repo_config = config_data['repository']

        # Валидация URL
        if 'url' not in repo_config:
            raise RepositoryURLError("Отсутствует параметр 'repository.url'")

        url = repo_config['url']
        if not url or not isinstance(url, str):
            raise RepositoryURLError("URL репозитория должен быть непустой строкой")
        self.repository_url = url

        # Валидация тестового режима
        if 'test_mode' not in repo_config:
            raise TestModeError("Отсутствует параметр 'repository.test_mode'")

        test_mode = repo_config['test_mode']
        if not isinstance(test_mode, bool):
            raise TestModeError("Параметр 'test_mode' должен быть булевым значением")
        self.test_mode = test_mode

        # Валидация локального пути (только для тестового режима)
        if self.test_mode:
            if 'local_path' not in repo_config:
                raise LocalPathError("В тестовом режиме требуется параметр 'repository.local_path'")

            local_path = repo_config['local_path']
            if not local_path or not isinstance(local_path, str):
                raise LocalPathError("Локальный путь должен быть непустой строкой")

            # Проверка существования директории (только если путь указан)
            if local_path and not os.path.exists(local_path):
                raise LocalPathError(f"Локальный путь не существует: {local_path}")

            self.local_path = local_path

    def get_all_parameters(self) -> Dict[str, Any]:
        """Получить все параметры конфигурации"""
        return {
            'package.name': self.package_name,
            'repository.url': self.repository_url,
            'repository.test_mode': self.test_mode,
            'repository.local_path': self.local_path if self.test_mode else "Не используется"
        }

    def display_parameters(self) -> None:
        """Вывод всех параметров в формате ключ-значение"""
        params = self.get_all_parameters()
        print("=== Параметры конфигурации ===")
        for key, value in params.items():
            print(f"{key}: {value}")
        print("==============================")