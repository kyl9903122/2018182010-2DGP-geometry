# Layer 0: Background Objects
# Layer 1: Foreground Objects
objects = [[], []]


def add_object(obj, layer):
    objects[layer].append(obj)


def add_objects(objs, layer):
    objects[layer] += objs


def remove_object(obj):
    for i in range(len(objects)):
        if obj in objects[i]:
            objects[i].remove(obj)
            del obj
            break


def clear():
    global objects
    for obj in all_objects():
        del obj
    objects.clear()
    objects = [[], []]

def all_objects():
    for i in range(len(objects)):
        for obj in objects[i]:
            yield obj

