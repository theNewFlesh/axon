#! /usr/bin/env python
# Alex Braun 06.30.2014

# ------------------------------------------------------------------------------
# The MIT License (MIT)

# Copyright (c) 2014 Alex Braun

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

'''
.. module:: panel
    :date: 06.30.2014
    :platform: Unix
    :synopsis: Client dependency graph panel
    
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from copy import copy, deepcopy
from collections import *

from axon.utilities.errors import *
from axon.client.core.dg import Component
# ------------------------------------------------------------------------------

class Panel():
    def __init__(self):
        self._index = []
        self._index_lut = {}
        self._values = []
        self._separator  = '__null__'
        self._index_item = '<-----'
        self._head       = '     |--- '
        self._tail       = ' -------> ' 
        self._branch     = '     |    '
    # --------------------------------------------------------------------------

    @property
    def index(self):
        return self._index

    @property
    def index_lut(self):
        return self._index_lut

    @property
    def values(self):
        return self._values

    @property
    def data(self):
        return zip(self._index, self._values)

    @property
    def width(self):
        return len(self._index[0]) + 1

    @property
    def height(self):
        return len(self._index)
    # --------------------------------------------------------------------------

    def nested_dict_to_matrix(self, data):
        sep = self._separator
        output = []
        def _nested_dict_to_matrix(data, name):
            for key, val in data.iteritems():
                new_key = name + sep + str(key)
                if type(val) is dict and val != {}:
                    output.append([new_key, self._index_item])
                    _nested_dict_to_matrix(val, new_key)
                else:
                    output.append([new_key, val])
        _nested_dict_to_matrix(data, sep)
        output = [[x[0].split(sep)[2:], x[1]] for x in output]
        return output

    def matrix_to_nested_dict(self, data):
        output = {}
        for row in data:
            keys = row[0]
            value = row[1]
            cursor = output
            for key in keys:
                # build dict with dummy value dicts
                try:
                    cursor = cursor[key]
                except KeyError:
                    if value != self._index_item:
                        cursor[key] = {'__value__': value}
                        cursor = cursor[key]
                    else:
                        cursor[key] = {}
                        cursor = cursor[key]
                
                # replace dummy dicts with real values
                cursor = output
                for key in keys:
                    if cursor[key].keys() == ['__value__']:
                        val = cursor[key]['__value__']
                        cursor[key] = val
                    cursor = cursor[key]
        return output

    def transpose(self, data):
        output = []
        for i in range(len(data[0])):
            new_row = []
            for row in data:
                new_row.append(row[i])
            output.append(new_row)
        return output

    def _add_spanning_branches(self, index):
        index =  self.transpose(index)
        new_index = []
        for row in index:
            new_row = row
            branches = []
            temp = []
            for i, item in enumerate(row):
                if item == self._head:
                    temp.append(i)
                elif item == '':
                    pass
                else:
                    temp = []
                if len(temp) == 2:
                    branches.append(temp)
                    temp = [temp[1]]

            for branch in branches:
                for i in range(branch[0] + 1, branch[1]):
                    new_row[i] = self._branch
            new_index.append(new_row)
        index = self.transpose(index)
        return index

    def read_nested_dict(self, data):
        data = copy(data)
        data = self.nested_dict_to_matrix(data)
        index = [x[0] for x in data]
        self._index_lut = index
        self._values = [x[1] for x in data]

        new_index = []
        for row in index:
            new_row = ['' for x in row[:-1]] # remove duplicate items
            new_row.append(self._head)       # add head item
            new_row.append(row[-1])          # append column name
            new_row = new_row[1:]            # remove first column
            new_index.append(new_row)
        index = new_index

        width = 0
        for item in index:
            if len(item) > width:
                width = len(item)

        # buffer index
        for item in index:
            while len(item) < width:
                item.append(self._tail)

        index = self._add_spanning_branches(index)
        self._index = index

    def to_nested_dict(self):
        data = zip(sef._index_lut, self._values)
        return self.matrix_to_nested_dict(data)

    def print_data(self, col_width=10, start=0, stop=-1):
        w = str(col_width)
        fmat1 = '{:<' + w + '.' + w + '}'
        fmat1 *= self.width
        fmat2 = '{:<' + w + '}'
        fmat2 *= self.width
        
        output = []
        for row in self.data[start:stop]:
            output = copy(row[0])
            output.append(row[1])
            try:
                print fmat1.format(*output)
            except:
                print fmat2.format(*output)

    def get_item(self, row):
        return self._values[row]

    def set_item(self, row, value):
        if slef.get_item(row) == self._index_item:
            target = self._index_lut[row]
            column = len(target) - 1
            target = target[-1]

            for row in self._index_lut:
                if len(row) >= column + 1:
                    if row[column] == target:
                        row[column] = value

            for row in self._index:
                if len(row) >= column + 1:
                    if row[column] == target:
                        row[column] = value

        else:
            self._values[row] = value
# ------------------------------------------------------------------------------

def main():
    '''
    Run help if called directly
    '''
    
    import __main__
    help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Panel']

if __name__ == '__main__':
    main()
