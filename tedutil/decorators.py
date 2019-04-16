def memoize(fn):
    cache = dict()

    def inner(kleidi):
        if kleidi not in cache:
            cache[kleidi] = fn(kleidi)
        return cache[kleidi]

    return inner
