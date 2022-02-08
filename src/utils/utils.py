import string
import random
from time import time


def random_file_name() -> str:
    """
    Function to create random file name
    :return: random file name
    """
    rand = string.ascii_uppercase + string.digits
    name = ''.join(random.sample(rand*6, 6))
    file_name = f"{name}_{time()}"
    return file_name
