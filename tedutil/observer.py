class Observable:
    def __init__(self):
        self.observers = list()

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def notify_objects(self):
        for observer in self.observers:
            observer.update(self)

    def __str__(self):
        return "Malakia1"


class Tes1:
    def __init__(self):
        self.val = 0

    def update(self, object):
        print("Object %s updated" % object)


class Tes2:
    def update(self, object):
        print("object %s" % object)


if __name__ == "__main__":
    obj = Observable()
    er1 = Tes1()
    er2 = Tes1()
    er3 = Tes2()
    obj.subscribe(er1)
    obj.subscribe(er2)
    obj.subscribe(er3)
    obj.notify_objects()
    obj.unsubscribe(er3)
    obj.notify_objects()
