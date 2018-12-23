import json


def sum_json(data, part2=False):
    """
    >>> sum_json([1,2,3])
    6
    >>> sum_json({"a":2,"b":4})
    6
    >>> sum_json([[[3]]])
    3
    >>> sum_json({"a":{"b":4},"c":-1})
    3
    >>> sum_json({"a":[-1,1]})
    0
    >>> sum_json([-1,{"a":1}])
    0
    >>> sum_json([])
    0
    >>> sum_json({})
    0
    >>> sum_json([1,2,3], True)
    6
    >>> sum_json([1,{"c":"red","b":2},3], True)
    4
    >>> sum_json({"d":"red","e":[1,2,3,4],"f":5}, True)
    0
    >>> sum_json([1,"red",5], True)
    6
    """
    total = 0
    nodes = [data]
    while nodes:
        current_node = nodes.pop(0)
        try:  # Is current node a list?
            nodes = current_node + nodes
        except TypeError:
            try: # Is current node a dict?
                if part2:
                    if 'red' in current_node.keys() or 'red' in current_node.values():
                        continue
                nodes = list(current_node.values()) + nodes
            except AttributeError:
                try: # Is current node an int?
                    total += current_node
                except TypeError:  # Must be a string
                    pass
    return total


def adventofcode():
    with open('12.json') as json_file:
        data = json.load(json_file)
    return sum_json(data), sum_json(data, True)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
