import os
import json


def check_dir_path(dir_path: str) -> None:
    if not isinstance(dir_path, str):
        raise ValueError("config dir must be a string - path to folder with config files")

    if not os.path.exists(dir_path):
        raise ValueError("specified path does not exist")

    if not os.path.isdir(dir_path):
        raise ValueError("specified path is not a directory")


def check_configs(dir_path: str) -> None:
    pass  # FIXME: добавить проверку


def get_dir_structure(dir_path: str) -> dict:
    dir_structure = dict()

    for root_path, dirs, files in os.walk(dir_path, topdown=False):
        root_name = os.path.basename(root_path)
        dir_structure[root_name] = list()

        for name in files:
            if name.endswith(".json"):
                dir_structure[root_name].append(os.path.join(root_path, name))

    return dir_structure


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

        check_configs(conf_dir)

        self.conf_dir = conf_dir

        self.conf_data = dict()

        self.read_configs()

    def read_configs(self):
        conf_structure = get_dir_structure(self.conf_dir)

        for group in conf_structure:
            self.conf_data[group] = list()
            group_elements = self.conf_data[group]

            for file_path in conf_structure[group]:
                with open(file_path) as file:
                    group_elements.extend(json.load(file))

    def get_config_data(self):
        return self.conf_data

    def get_category_config(self, category: str) -> dict:
        return self.conf_data[category]
