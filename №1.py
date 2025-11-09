import toml
import sys
import os
import subprocess

def load_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Конфигурационный файл не найден: {file_path}")
    try:
        config = toml.load(file_path)
        return config
    except toml.TomlDecodeError as e:
        raise ValueError(f"Ошибка парсинга TOML: {e}")

def validate_config(config):
    # Проверка наличия разделов и обязательных ключей
    required_sections = ['package', 'repository', 'mode']
    for section in required_sections:
        if section not in config:
            raise KeyError(f"Отсутствует раздел '{section}' в конфигурации")
    # Проверка конкретных ключей
    if 'name' not in config['package']:
        raise KeyError("Отсутствует ключ 'name' в разделе [package]")
    if 'url' not in config['repository']:
        raise KeyError("Отсутствует ключ 'url' в разделе [repository]")
    if 'operation' not in config['mode']:
        raise KeyError("Отсутствует ключ 'operation' в разделе [mode]")

    # Дополнительные проверки (например, URL допустим или нет)
    url = config['repository']['url']
    if not (url.startswith("http://") or url.startswith("https://") or os.path.exists(url)):
        raise ValueError(f"Некорректный URL или путь: {url}")

    # Проверка режима
    mode = config['mode']['operation']
    if mode not in ['read-only', 'write', 'test']:
        raise ValueError(f"Недопустимый режим operation: {mode}")

def print_config(config):
    for section, params in config.items():
        for key, value in params.items():
            print(f"{section}.{key} = {value}")

def main():
    config_path = 'config.toml'
    try:
        config = load_config(config_path)
        validate_config(config)
        print("Настраиваемые параметры:")
        print_config(config)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

    # После успешного выполнения можно завершить работу

if __name__ == "__main__":
    main()
