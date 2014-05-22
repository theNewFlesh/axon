#! /usr/bin/env python

# Alex Braun 12.29.2013
# >> INSERT LICENSE HERE <<

'''
.. module:: cache
	:date: 12.29.2013
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













