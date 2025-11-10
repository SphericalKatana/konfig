import json
import sys
import urllib.request
import urllib.error


def get_package_info(package_name):
    """Получает метаданные пакета с PyPI через JSON API."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Ошибка: пакет '{package_name}' не найден на PyPI.", file=sys.stderr)
        else:
            print(f"Ошибка HTTP при запросе к PyPI: {e}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Ошибка сети: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Ошибка: не удалось разобрать JSON-ответ от PyPI.", file=sys.stderr)
        sys.exit(1)


def extract_direct_dependencies(info):
    """Извлекает прямые зависимости из метаданных пакета."""
    requires_dist = info.get("info", {}).get("requires_dist")
    if not requires_dist:
        return []
    # Фильтруем только строки без маркеров окружения (например, ; python_version >= "3.6")
    # Для упрощения этапа выводим все зависимости из requires_dist
    return requires_dist


def main():
    if len(sys.argv) != 2:
        print("Использование: python fetch_dependencies.py <имя_пакета>", file=sys.stderr)
        sys.exit(1)

    package_name = sys.argv[1].strip()
    if not package_name:
        print("Ошибка: имя пакета не может быть пустым.", file=sys.stderr)
        sys.exit(1)

    print(f"Получение зависимостей для пакета: {package_name}...")
    data = get_package_info(package_name)
    dependencies = extract_direct_dependencies(data)

    if dependencies:
        print("\nПрямые зависимости:")
        for dep in dependencies:
            print(f" - {dep}")
    else:
        print("\nПрямые зависимости не найдены.")


if __name__ == "__main__":
    main()


###ВВОДИТЬ НАЗВАНИЯ ПАКЕТОВ ПЕРЕД ЗАПУСКОМ В EDIT CONFIGURATION. ПРИМЕРЫ:requests, numpy
