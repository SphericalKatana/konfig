import sys
import argparse
from config import DependencyVisualizerConfig
from errors import *


def main():
    parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей пакетов')
    parser.add_argument('--config', '-c', default='config.toml',
                        help='Путь к конфигурационному файлу (по умолчанию: config.toml)')

    args = parser.parse_args()

    try:
        # Загрузка и валидация конфигурации
        config = DependencyVisualizerConfig(args.config)

        # Вывод всех параметров (требование этапа 1)
        config.display_parameters()

        # Здесь будет основная логика визуализации графа зависимостей
        print(f"\nАнализ пакета: {config.package_name}")
        if config.test_mode:
            print(f"Режим: тестовый (локальный путь: {config.local_path})")
        else:
            print(f"Режим: рабочий (URL: {config.repository_url})")

    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПрервано пользователем", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()