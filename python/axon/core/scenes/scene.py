#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: scene
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Dependency graph scene
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import re
import copy
from collections import OrderedDict

from axon.utilities.errors import _check_kwargs
from axon.dependency.graph.nodes.components.dg import DG
from axon.utilities.informer import Informer
# ------------------------------------------------------------------------------

class Scene(DG):
	def __init__(self, name, owner=None, **options):
		super(Scene, self).__init__(name, owner=owner, **options)
		self._class = 'Scene'
		self._name = name
		self._owner = owner
		self._node_library = OrderedDict()
		self._nodes = OrderedDict()
		self._informer = Informer(name + 'Informer', owner=self)
		self._informer.create_log('connection')
		self._informer.create_log('node')
		self._informer.activate_log('connection')
		self._informer.activate_log('node')
	# --------------------------------------------------------------------------
	
	def get_informer(self):
		return self._informer
	# --------------------------------------------------------------------------

	def add_node_to_library(self, name, node):
		self._node_library[name] = node

	def remove_node_from_library(self, name):
		del self._node_library[name]

	def get_node_from_library(self, name):
		return self._node_library[name]

	def get_nodes_from_library(self):
		return self._node_library.values()

	def list_nodes_from_library(self):
		for key, val in self._node_library.iteritems():
			print key, ':', val
	# --------------------------------------------------------------------------
		
	def create_node(self, node_library_name='~!node_library_name'):
		_check_kwargs(node_library_name)

		# INFORMER HOOK
		message = 'create_node', node_library_name
		self.get_informer().log('node', message=message)
		# ----------------------------------------------------------------------

		name = self.generate_node_name(node_library_name)
		node_class = self.get_node_from_library(node_library_name)
		self._nodes[name] = node_class(name, self)
		return self.get_node(name)

	def destroy_node(self, name):
		# INFORMER HOOK
		message = 'destroy_node', self.get_name(), name
		self.get_informer().log('node', message=message)
		# ----------------------------------------------------------------------
		
		del self._nodes[name]
	
	def connect_ports(self, out_port='~!out_port', in_port='~!in_port'):
		_check_kwargs(out_port, in_port)
		
		# INFORMER HOOK
		message = ('connect_ports', out_port.get_owner_node().get_name(),
		out_port.get_name(), in_port.get_owner_node().get_name(), in_port.get_name() )
		self.get_informer().log('node', message=message)
		# ----------------------------------------------------------------------
		
		in_port.connectPort(out_port)

	def disconnect_ports(self, in_port='~!in_port'):
		_check_kwargs(in_port)

		# INFORMER HOOK
		message = 'disconnect_ports', in_port.get_owner_node().get_name(), in_port.get_name()
		self.get_informer().log('node', message=message)
		# ----------------------------------------------------------------------

		in_port.disconnect_port()
	
	def get_node(self, name):
		return self._nodes[name]

	def get_nodes(self):
		return self._nodes.values()

	def list_nodes(self):
		for key, val in self._nodes.iteritems():
			print key, ':', val

	def generate_node_name(self, node_library_name='~!node_library_name'):
		_check_kwargs(node_library_name)
		node_re = re.compile(node_library_name)
		num = 1
		for key in self._nodes:
			found = node_re.search(key)
			if found:
				num += 1
		return node_library_name + str(num)
# ------------------------------------------------------------------------------

class MainScene(Scene):
    def __init__(self, name, owner=None, **options):
        super(MainScene, self).__init__(name, owner=owner, **options)
        self._class = 'MainScene'
        self._name = name
        self._owner = owner
        self._node_library = OrderedDict()
        self._nodes = OrderedDict()
        self._scenes = {} 
    # --------------------------------------------------------------------------
	
    def add_scene(self, name, scene):
        scene._owner = self
        self._scenes[name] = scene

    def get_scene(self, name):
        return self._scene[name]

    def get_scenes(self):
        return self._scenes.values()

    def list_scenes(self):
        for key, val in self._scenes.iteritems():
            print key, ':', val

    def aggregate_all_library_nodes(self):
        for scene in self.get_scenes():
        	for name, node in scene._node_library.iteritems():
        		self.add_node_to_library(name, node)
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Scene', 'MainScene']

if __name__ == '__main__':
	main()