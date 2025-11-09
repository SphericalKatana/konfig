import os
import subprocess

def read_graph_from_file(filepath):
    graph = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            package, deps = line.split(':')
            package = package.strip()
            dependencies = [d.strip() for d in deps.split(',')] if deps.strip() else []
            graph[package] = dependencies
    return graph

def dfs(graph, node, visited, rec_stack, dependencies):
    if node in rec_stack:
        print(f"Обнаружен цикл при обработке {node}")
        return
    if node in visited:
        return
    visited.add(node)
    rec_stack.add(node)
    for dep in graph.get(node, []):
        dependencies.add(dep)
        dfs(graph, dep, visited, rec_stack, dependencies)
    rec_stack.remove(node)

def build_dependency_graph(graph, start_node):
    dependencies = set()
    visited = set()
    rec_stack = set()
    dfs(graph, start_node, visited, rec_stack, dependencies)
    return dependencies

def main():
    mode = input("Выберите режим (реальный репозиторий / тестовый файл, введите 'file' или 'repo'): ").strip()
    if mode == 'file':
        filepath = input("Введите путь к файлу описания графа: ").strip()
        graph = read_graph_from_file(filepath)
        start_node = input("Введите название пакета для анализа (большие буквы): ").strip()
    elif mode == 'repo':
        # Здесь можно вставить вызов предыдущего этапа для получения графа
        # Для примера, создадим тестовый граф вручную
        graph = {
            'A': ['B', 'C'],
            'B': ['C', 'D'],
            'C': ['D'],
            'D': []
        }
        start_node = input("Введите название пакета для анализа: ").strip()
    else:
        print("Некорректный режим.")
        return

    print(f"Анализ пакета: {start_node}")
    deps = build_dependency_graph(graph, start_node)
    print("Полные транзитивные зависимости:")
    for dep in deps:
        print(f" - {dep}")

    # Сохраняем результат в файл
    result_file = 'full_dependencies.txt'
    with open(result_file, 'w') as f:
        f.write(f"Зависимости пакета {start_node}:\n")
        for dep in deps:
            f.write(dep + '\n')


if __name__ == "__main__":
    main()