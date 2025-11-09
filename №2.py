import os
import subprocess
import tempfile
import shutil

def clone_repo(repo_url):
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.check_call(['git', 'clone', repo_url, temp_dir])
        return temp_dir
    except subprocess.CalledProcessError:
        shutil.rmtree(temp_dir)
        raise

def find_file(repo_dir, filenames):
    for root, dirs, files in os.walk(repo_dir):
        for filename in filenames:
            if filename in files:
                return os.path.join(root, filename)
    return None

def parse_requirements_txt(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    dependencies = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return dependencies

def parse_setup_py(filepath):
    dependencies = []
    with open(filepath, 'r') as f:
        content = f.read()
    # Простая парсинг: ищем install_requires = [...]
    import re
    match = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.S)
    if match:
        deps_str = match.group(1)
        deps = re.findall(r'[\'\"](.*?)[\'\"]', deps_str)
        dependencies.extend(deps)
    return dependencies

def parse_pyproject_toml(filepath):
    dependencies = []
    try:
        import toml
    except ImportError:
        print("Для парсинга pyproject.toml требуется библиотека toml.")
        return dependencies
    data = toml.load(filepath)
    # В зависимости от формата, ищем разделы
    if 'project' in data and 'dependencies' in data['project']:
        dependencies.extend(data['project']['dependencies'])
    elif 'tool' in data and 'poetry' in data['tool'] and 'dependencies' in data['tool']['poetry']:
        dependencies.extend(data['tool']['poetry']['dependencies'].keys())
    return dependencies

def main():
    repo_url = input("Введите URL репозитория: ")
    try:
        repo_dir = clone_repo(repo_url)
        print(f"Репозиторий склонирован в {repo_dir}")
    except Exception as e:
        print(f"Ошибка при клонировании репозитория: {e}")
        return

    # Ищем файлы
    setup_py = find_file(repo_dir, ['setup.py'])
    requirements_txt = find_file(repo_dir, ['requirements.txt'])
    pyproject_toml = find_file(repo_dir, ['pyproject.toml'])

    dependencies = []

    if requirements_txt:
        dependencies.extend(parse_requirements_txt(requirements_txt))
    elif setup_py:
        dependencies.extend(parse_setup_py(setup_py))
    elif pyproject_toml:
        dependencies.extend(parse_pyproject_toml(pyproject_toml))
    else:
        print("Не найдены файлы с зависимостями.")
        shutil.rmtree(repo_dir)
        return

    # Вывод зависимостей
    print("Прямые зависимости пакета:")
    for dep in dependencies:
        print(f" - {dep}")

    # Сохраняем результат в файл
    deps_file = os.path.join(repo_dir, 'dependencies.txt')
    with open(deps_file, 'w') as f:
        for dep in dependencies:
            f.write(dep + '\n')

    # Коммит изменений
    try:
        subprocess.check_call(['git', 'add', deps_file], cwd=repo_dir)
        subprocess.check_call(['git', 'commit', '-m', 'Добавлены зависимости пакета'], cwd=repo_dir)
        print("Зависимости сохранены и зафиксированы.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении git-команд: {e}")
    finally:
        # Можно оставить репозиторий или удалить временную папку
        shutil.rmtree(repo_dir)

if __name__ == "__main__":
    main()