
class Singletone:
    instances = {}

    def __new__(cls, classname, parents, attributes):
        creat_type = type(classname, parents, attributes)
        if classname not in Singletone.instances:
            instance = creat_type()
            Singletone.instances[classname] = instance

        def __new__(self):
            return Singletone.instances[classname]
        creat_type.__new__ = __new__
        return creat_type
