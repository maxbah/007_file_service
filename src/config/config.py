from src.utils.python_interface import Singletone
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class Config(metaclass=Singletone):

    def __init__(self):
        self.sig_alg = 'md5'
        self.public_exponent = 55555
        self.key_size = 1024
        self.config_data = None

    def load(self, filename):
        self.config_data = configparser.ConfigParser()
        data = self.config_data.read(filename)
        return data

    def signature_algo(self):
        for key in self.config_data['SIGNATURE_SECTION']:
            if key == 'Signature'.lower():
                self.sig_alg = self.config_data['SIGNATURE_SECTION']['Signature']
        print("SIG ALG:", self.sig_alg)
        return self.sig_alg

    def get_crypto_section_params(self):
        """
        Get Public_exponent and Key_size from config.ini
        Default value in __init__
        :return: tuple
        """
        for key in self.config_data['CRYPTO_SECTION']:
            if key == 'Public_exponent'.lower():
                self.public_exponent = self.config_data['CRYPTO_SECTION']['Public_exponent']
            if key == 'Key_size'.lower():
                self.key_size = self.config_data['CRYPTO_SECTION']['Key_size']
        print("Public_exponent: ", self.public_exponent, ' Key_size: ', self.key_size)
        return self.public_exponent, self.key_size
