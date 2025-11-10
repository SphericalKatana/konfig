import os
import subprocess
import sys


def read_graph_from_file(filepath):
    """Читает граф зависимостей из файла. Формат: Package: dep1, dep2, ..."""
    graph = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' not in line:
                    raise ValueError(f"Некорректный формат в строке {line_num}: '{line}'")
                package, deps_part = line.split(':', 1)
                package = package.strip()
                if not package:
                    raise ValueError(f"Пустое имя пакета в строке {line_num}")
                dependencies = [d.strip() for d in deps_part.split(',') if d.strip()]
                graph[package] = dependencies
        return graph
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def dfs(graph, node, visited, rec_stack, dependencies):
    """DFS для сбора транзитивных зависимостей с обнаружением циклов."""
    if node in rec_stack:
        # Цикл обнаружен: узел уже в текущем стеке вызовов
        raise RecursionError(f"Циклическая зависимость обнаружена: '{node}' входит в цикл.")
    if node in visited:
        return  # Уже обработан — выходим

    # Добавляем в стек рекурсии
    rec_stack.add(node)
    visited.add(node)

    # Обрабатываем зависимости
    for dep in graph.get(node, []):
        dependencies.add(dep)
        dfs(graph, dep, visited, rec_stack, dependencies)

    # Убираем из стека рекурсии при выходе
    rec_stack.remove(node)


def build_dependency_graph(graph, start_node):
    """Возвращает множество транзитивных зависимостей или выбрасывает исключение при цикле."""
    if start_node not in graph:
        raise KeyError(f"Пакет '{start_node}' не найден в графе зависимостей.")
    dependencies = set()
    visited = set()
    rec_stack = set()
    dfs(graph, start_node, visited, rec_stack, dependencies)
    return dependencies


def commit_result_to_git(filename, package_name):
    """Добавляет файл в git и делает коммит."""
    try:
        subprocess.run(['git', 'add', filename], check=True)
        commit_message = f"feat: добавлены транзитивные зависимости для пакета {package_name}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"Результат сохранён в репозиторий коммитом: {commit_message}")
    except subprocess.CalledProcessError:
        print("Предупреждение: не удалось выполнить git commit. Убедитесь, что вы в git-репозитории.")


def main():
    print("Анализатор транзитивных зависимостей пакетов")
    mode = input("Выберите режим ('file' — тестовый файл, 'repo' — реальный репозиторий): ").strip().lower()

    if mode == 'file':
        filepath = input("Введите путь к файлу описания графа: ").strip()
        graph = read_graph_from_file(filepath)
        start_node = input("Введите название пакета для анализа (латинские заглавные буквы): ").strip()
        if not start_node.isalpha() or not start_node.isupper():
            print("Предупреждение: имя пакета должно быть заглавными латинскими буквами.")
    elif mode == 'repo':
        # Заглушка для будущей интеграции с реальным репозиторием
        graph = {
            'A': ['B', 'C'],
            'B': ['C', 'D'],
            'C': ['D'],
            'D': []
        }
        start_node = input("Введите название пакета для анализа: ").strip()
    else:
        print("Некорректный режим. Используйте 'file' или 'repo'.")
        return

    print(f"\nАнализ пакета: {start_node}")
    try:
        deps = build_dependency_graph(graph, start_node)
        print("Полные транзитивные зависимости:")
        if deps:
            for dep in sorted(deps):
                print(f" - {dep}")
        else:
            print(" - Нет зависимостей")

        # Сохраняем результат в файл
        result_file = 'full_dependencies.txt'
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"Зависимости пакета {start_node}:\n")
            for dep in sorted(deps):
                f.write(dep + '\n')
        print(f"\nРезультат сохранён в файл: {result_file}")

        # Коммитим в git
        commit_result_to_git(result_file, start_node)

    except KeyError as e:
        print(f"Ошибка: {e}")
    except RecursionError as e:
        print(f"Критическая ошибка: {e}")
        print("Программа завершена из-за циклической зависимости.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
