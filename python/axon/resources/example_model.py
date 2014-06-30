#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: example_model
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Example model for Axon testing
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

class Example():
	def __init__(self, name, data=None):
		self._name = name
		self._data = data

	@property
	def data(self):
		return self._data

	def set_data(self, data):
		self._data = data

	def add_data(self, data):
		output = self._data + data
		self._data = output
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''

	import __main__
	help(__main__)

__all__ = ['Example']

if __name__ == '__main__':
	main()