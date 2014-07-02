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
.. module:: scene
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Client dependency graph scene
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import re
import copy
import importlib

from axon.client.core.dg import DG
from axon.client.core.informer import SceneInformer
from axon.client.core.node import Node
# ------------------------------------------------------------------------------

class Scene(DG):
	def __init__(self, spec, owner):
		super(Scene, self).__init__(spec, owner)
		self._cls = 'Scene'
	# --------------------------------------------------------------------------

	@property
	def informer(self):
		return self._map['informer']

	@property
	def sources(self):
		return self._map['sources']

	@property
	def nodes(self):
		return self._map['nodes']
	# --------------------------------------------------------------------------

	def build(self, spec):
		self._map['name'] = spec['name']
		self._map['informer'] = self.create_informer(spec['informer'])
		self._map['sources'] = {}
		for cspec in spec['sources']:
			create_class(cspec)
		self._map['nodes'] = {}
		for nspec in spec['nodes']:
			create_node(nspec)
	# --------------------------------------------------------------------------

	def create_node_name(self, name):
		node_re = re.compile(name)
		num = 1
		for key in self.nodes:
			found = node_re.search(key)
			if found:
				num += 1
		return name + str(num)

	def create_node(self, spec):
		spec['name'] = self.create_node_name(spec['name'])

		for type_ in spec['packages'].values():
			if type_:
				for pspec in type_.values():
					pspec['class'] = self.create_class(pspec['source'])
				
		node = Node(spec, self)
		self.nodes[node.name] = node
		return node

	def create_informer(self, spec):
		informer = SceneInformer(spec, self)
		return informer

	def destroy_node(self, node_name):
		del self.nodes[node_name]

	def update_instruments(self, spec, node):
		node = self.nodes[spec['name']]
		node.update_instruments(spec)

	def update_informer(self, spec, node):
		node = self.nodes[spec['name']]
		node.update_informer(spec)

	def rebuild(self, spec, node):
		node = self.nodes[spec['name']]
		node.build(spec)

	def connect_ports(self, out_port, in_port):	
		in_port.connect(out_port)

	def disconnect_port(self, in_port):
		in_port.disconnect()
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Scene']

if __name__ == '__main__':
	main()