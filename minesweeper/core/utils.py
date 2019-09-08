
class Factory:

    @staticmethod
    def instance(obj_type, BaseClass, DefaultClass, *args, **kwargs):
        for ChildClass in BaseClass.__subclasses__():
            if ChildClass.is_type(obj_type):
                return ChildClass(*args, **kwargs)

        return DefaultClass(*args, **kwargs)
