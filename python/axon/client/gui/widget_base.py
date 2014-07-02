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
.. module:: widget_base
	:date: 06.30.2014
	:platform: Unix
	:synopsis: Client dependency graph widget base
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import copy
from axon.utilities.errors import *
from axon.utilities.utils import *
# ------------------------------------------------------------------------------

class WidgetBase(Component):
	def __init__(self, spec, owner):
		super(WidgetBase, self).__init__(spec, owner)
		self._cls = 'WidgetBase'
		self._spec = {}
		self._map = {}
		self._owner = owner
		self._widget = None
		self._widget_classes = {    'spinbox': "QSpinBox", 
							    'radiobutton': "QRadioButton"}
		self.build(spec)
	# --------------------------------------------------------------------------
	
	@property
	def spec(self):
		return self._spec

	@property
	def map(self):
		return self._map
	
	@property
	def owner(self):
		return self._owner

	@property
	def name(self):
		return self._map['name']

	@property
	def widget_type(self):
		return self._map['widget_type']

	@property
	def widget_classes(self):
		return self._widget_classes

	@property
	def value(self):
		return self._map['value']

	@property
	def default(self):
		return self._map['value']

	@property
	def widget(self):
		return self._widget
	# --------------------------------------------------------------------------
	
	def build(self, spec):
		self._spec = spec
		self._map['name'] = spec['name']
		self._map['widget_type'] = self.widget_classes[spec['widget_type']]
		self._map['value'] = spec['value']
		self._map['default'] = spec['default']
		# self._widget = self.widget_type(name=self.name, default=self.default, value=self.value) 
	# --------------------------------------------------------------------------
	
	def set_name(self, name):
		self._spec['name'] = name
		self.build(self.spec)

	def set_widget_type(self, widget_type):
		self._spec['widget_type'] = widget_type
		self.build(self.spec)

	def set_value(self, value):
		self._spec['value'] = value
		self.build(self.spec)

	def set_default(self, value):
		self._spec['default'] = value
		self.build(self.spec)
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['WidgetBase']

if __name__ == '__main__':
	main()