#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: utils
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Library of utilities
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

import re
from collections import OrderedDict
# ------------------------------------------------------------------------------

class Base(object):
	'''
	Dummy class for argument passing
	'''
	
	def __init__(self):
		self._cls = 'Base'

	@property
	def cls(self):
		return self._cls

	def _print_public(self):
		non_public_re = re.compile('^_')
		for item in dir(self):
			found = non_public_re.match(item)
			if not found:
				print item

	def _print_semi_private(self):
		semi_private_re = re.compile('^_[^_]+')
		for item in dir(self):
			found = semi_private_re.match(item)
			if found:
				print item

	def _print_private(self):
		private_re = re.compile('^__')
		for item in dir(self):
			found = private_re.match(item)
			if found:
				print item
# ------------------------------------------------------------------------------

def is_iterable(item):
	try:
		result = iter(item)
	except TypeError:
		return False
	return True

def spec_to_ordereddict(spec):
    order = sorted(spec.keys())
    new_dict = OrderedDict()
    for key in order:
        temp = spec[key]
        new_key = temp.keys()[0]
        new_val = temp[new_key]
        new_dict[new_key] = new_val
    return new_dict
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Base', 'is_iterable', 'spec_to_ordereddict']

if __name__ == '__main__':
	main()