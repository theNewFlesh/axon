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
.. module:: cache
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Python dependency graph cache
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import os
import copy
from collections import OrderedDict, deque
import jsonpickle

from axon.utilities.errors import *
from axon.dependency.graph.caches.components.dg import DG
# ------------------------------------------------------------------------------

class Cache(DG):
	def __init__(self, name, owner, *args, **kwargs):
		super(Cache, self).__init__(name, owner, *args, **kwargs)
		self._class = 'Cache'
		self._name = name
		self._owner = owner
		self._stack = OrderedDict()
		self._count = 0
		self._cache_directory = None

	def add_item(self, name, item):
		item_name = str(self._count).zfill(4) + '_' + name
		self._stack[item_name] = jsonpickle.encode(item)
		self._count += 1

	def get_item(self, name):
		temp = []
		name_re = re.compile(name)
		for item in self._stack:
			found = name_re.search(item):
			if found:
				temp.append(item)
		item = self._stack[max(temp)]
		return jsonpickle.decode(item)

	def dump(self):
		for name, item in self._stack.iteritems():
			file_name = name + '.json'
			full_path = os.join(self._cache_directory, file_name)		
			with open(full_path, 'w+') as cache:
				cache.write(item)

		self._stack.clear()

	def deepcopy_package(self, package):
		pkg = copy.copy(package)
	 	instance = copy.copy(package.get_instance())
	    pkg.set_instance(instance)
	    return pkg













