# class Signer(type):
#     signers = {}
#
#     def __new__(cls, classname, parents, attributes):
#         if "__call__" not in attributes:
#             raise Exception(f"Signer class must implement {classname}.__call__ function")
#         signer_class = type(classname, parents, attributes)
#         if "label" not in attributes:
#             signer_class.label = classname.lower()
#         Signer.signers[signer_class.label] = signer_class
#         return signer_class
#
#     @staticmethod
#     def get_signer(label):
#         return Signer.signers[label]
#
#
# class Md5Signer(metaclass=Signer):
#     label = "md5"
#
#     def __call__(self, data):
#         return hashlib.md5(data.encode()).hexdigest()
#
#
# class Sha512Signer(metaclass=Signer):
#     def __call__(self, data):
#         return hashlib.sha512(data.encode()).hexdigest()
#
#
# class Sha256Signer(metaclass=Signer):
#     def __call__(self, data):
#         return hashlib.sha512(data.encode()).hexdigest()
#
#
# class Sha128Signer(metaclass=Signer):
#     def __call__(self, data):
#         return hashlib.sha128(data.encode()).hexdigest()
#
#
# class X(metaclass=Signer):
#     def __call__(self, data):
#         pass
#
#
# #
# # print(f"Md5Signer.label = {Md5Signer.label}")
# # print(f"Sha256Signer.label = {Sha256Signer.label}")
# # print(f"X.label = {X.label}")
# # print(f"signers = {Signer.get_signer('md5')}")
# #
#
# # file_service.create_signed_file("blabla", Sha512Signer())
#
# def read_signed_file(filename):
#     data = file_service.read_file(filename)
#     for label in Signer.signers:
#         sig_filename = f"{filename}.{label}"
#         if os.path.exists(sig_filename):
#             signer = Signer.get_signer(label)
#             with open(sig_filename, "r") as sig_file:
#                 actual_sig = signer(data)
#                 expected_sig = sig_file.read()
#                 if actual_sig == expected_sig:
#                     return data
#                 else:
#                     raise Exception("File broken")

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
