class ConfigError(Exception):
    """Базовое исключение для ошибок конфигурации"""
    pass

class PackageNameError(ConfigError):
    """Ошибка в имени пакета"""
    pass

class RepositoryURLError(ConfigError):
    """Ошибка в URL репозитория"""
    pass

class TestModeError(ConfigError):
    """Ошибка в настройке тестового режима"""
    pass

class LocalPathError(ConfigError):
    """Ошибка в пути к локальному репозиторию"""
    pass

class ConfigFileError(ConfigError):
    """Ошибка чтения конфигурационного файла"""
    pass