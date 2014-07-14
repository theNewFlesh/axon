class Panel():
    def __init__(self):
        self._spec = {}
        self._map = []
        self._values = []
        self._index = []
        self._data = []
    
    @property
    def values(self):
        return self._values
    
    @property
    def index(self):
        return self._index
    
    @property
    def map(self):
        return self._map
    
    @property
    def data(self):
        return zip(self._index, self._values) 
    
    @property
    def width(self):
        return len(self.data[0])
    
    @property
    def height(self):
        return len(self._index)
    
    def read_nested_dict(self, item, null='null', head_null='', tail_null='-->'):
        separator = '__null__'
        data = []
        def _flatten_nested_dict(item, name):
            for key, val in item.iteritems():
                if type(val) is dict and val != {}:
                    data.append([name + separator + str(key), null])
                    _flatten_nested_dict(val, name + separator + str(key))
                else:
                    data.append([name + separator + str(key), val])
        _flatten_nested_dict(item, separator)

        new_data = []
        header = len(separator) * 2
        for item in data:
            new_data.append([item[0][header:], item[1]])
        data = new_data

        index = [x[0].split(separator) for x in data]
        self._map = index
        new_index = []
        for row in index:
            new_row = [head_null for x in row[:-1]]
            new_row.append(row[-1])
            new_index.append(new_row)
        index = new_index

        width = 0
        for item in index:
            if len(item) > width:
                width = len(item)
        for item in index:
            while len(item) < width:
                item.append(tail_null)

        values = [x[1] for x in data]
        self._values = values
        self._index = index
    
    def print_data(self, width=10):
        w = str(width)
        fmat1 = '{:<' + w + '.' + w + '}'
        fmat1 *= self.width
        fmat2 = '{:<' + w + '}'
        fmat2 *= self.width
        for row in self.data:
            output = row[0]
            output.append(row[1])
            try:
                print fmat1.format(*output)
            except:
                print fmat2.format(*output)
        
#     def transpose(self, inplace=False):
#         data = []
#         for i in range(len(self.data[0])):
#             new_row = []
#             for row in data:
#                 new_row.append(row[i])
#             data.append(new_row)
        
#         if inplace:
#             self._data = data        
#         return data

x = Panel()
x.read_nested_dict(spec)

class Widget():
    def __init__(self, spec, lookup):
        loc = spec
        for key in lookup[:-1]:
            loc = loc[key]
        self._lookup = {'loc': loc, 'key': lookup[-1]}
    
    def get_value(self):
        lu = self._lookup
        return lu['loc'][lu['key']]
    
    def set_value(self, value):
        lu = self._lookup
        lu['loc'][lu['key']] = value