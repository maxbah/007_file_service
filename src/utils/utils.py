import string
import random
from time import time
from datetime import datetime


def random_file_name() -> str:
    """
    Function to create random file name
    :return: random file name
    """
    rand = string.ascii_uppercase + string.digits
    name = ''.join(random.sample(rand*6, 6))
    file_name = f"{name}_{time()}"
    return file_name


def get_human_date(date: float) -> str:
    """
    Function to get human date
    :param date: data in ms
    :return: date
    """
    human_date = datetime.fromtimestamp(date).strftime("%b %d %Y %H:%M:%S")
    return human_date
