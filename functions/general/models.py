class BodyObject(object):
    def __init__(self, *initial_attrs, **kwargs):
        for dictionary in initial_attrs:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)