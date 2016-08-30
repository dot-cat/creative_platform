import os


def check_dir_path(dir_path: str) -> None:
    if not isinstance(dir_path, str):
        raise ValueError("config dir must be a string - path to folder with config files")

    if not os.path.exists(dir_path):
        raise ValueError("specified path does not exist")

    if not os.path.isdir(dir_path):
        raise ValueError("specified path is not a directory")


def check_configs(dir_path: str) -> None:
    pass  # FIXME: добавить проверку


class Model(object):
    """
    Класс, который содержит представление всей системы и параметры всех компонентов
    """
    def __init__(self, conf_dir: str):
        """
        Конструктор класса
        :param conf_dir: путь к конфиг-файлам
        """
        check_dir_path(conf_dir)

        self.conf_dir = conf_dir

    def parse_controllable(self) -> list:
        pass
