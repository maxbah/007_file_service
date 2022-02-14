
# Task
# Create module crypto
# Create file in module crypto : signature.py
# Create SignatureFactory meta class
# SignatureFactory should check if SignatureClass contains "__call__" function
# SignatureFactory should add label to class if labled is not already specified
# Create 2 signatures algos : md5, sha512
# Create read_signed_file function in file service
# Create create_signed_file function in file service
# Signature should be stored near the file with same name and extension as also label

import hashlib


class SignatureFactory(type):
    signers = {}

    def __new__(cls, classname, parents, attributes):
        if "__call__" not in attributes:
            raise Exception(f'Class must have {classname}.__call__ function')
        signer = type(classname, parents, attributes)
        if "label" not in attributes:
            signer.label = classname.lower()
        SignatureFactory.signers[signer.label] = signer()
        return signer

    @staticmethod
    def get_signer(label):
        return SignatureFactory.signers[label]


class Md5umSign(metaclass=SignatureFactory):
    label = "md5"

    def __call__(self, data):
        return hashlib.md5(data.encode()).hexdigest()


class Sha512Sign(metaclass=SignatureFactory):
    label = "sha512"

    def __call__(self, data):
        return hashlib.sha512(data.encode()).hexdigest()
