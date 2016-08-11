from pprint import pprint
import gc


def print_referrers(instance):
    """
    Print referrers of object instance
    :param instance: studied instance
    :return: None
    """
    print(instance)
    pprint(gc.get_referents(instance))
    print()
