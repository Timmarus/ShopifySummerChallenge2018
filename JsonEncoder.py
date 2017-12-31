import json
import collections
from Menu import Menu

class JsonEncoder(json.JSONEncoder):
    """Use with json.dumps to allow Python sets to be encoded to JSON

    Example
    -------

    import json

    data = dict(aset=set([1,2,3]))

    encoded = json.dumps(data, cls=JSONSetEncoder)
    decoded = json.loads(encoded, object_hook=json_as_python_set)
    assert data == decoded     # Should assert successfully

    Any object that is matched by isinstance(obj, collections.Set) will
    be encoded, but the decoded value will always be a normal Python set.

    Credit to NeilenMarais of StackOverflow
    https://stackoverflow.com/questions/8230315/how-to-json-serialize-sets
    """

    def default(self, obj):
        if isinstance(obj, collections.Set):
            return list(obj)
        elif isinstance(obj, Menu):
            return obj.id
        else:
            return json.JSONEncoder.default(self, obj)
